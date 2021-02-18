import mysql.connector
import requests
import time
import datetime
import random
from bs4 import BeautifulSoup
import module_news_comTag
import module_news_govTag
import module_news_topicTag
import module_logWriter as lw


def minorRandomPause():
    randomTime = random.randint(600, 900)
    lw.log_writer('东方财富脚本进入休眠' + str(randomTime) + '秒')
    time.sleep(randomTime)

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                user='rayshi',
                                password='Rayshi1994!',
                                database='ttd',
                                auth_plugin='mysql_native_password')

    
    print('DB is connected')
    print()
    return mydb

def parsingContent(link):
    fullLink = 'http://fund.eastmoney.com/a/' + link
    p = requests.get(fullLink)
    s = BeautifulSoup(p.content, features = 'html.parser')

    lw.log_writer('东方财富脚本开始爬取' + fullLink)

    title = ''
    content = ''

    try: # 爬取标题
        title = s.find('h1').text.replace('\n', '')
    except:
        lw.log_writer('东方财富脚本爬取标题错误')

    try:
        contentList = s.findAll('div', {'id': 'ContentBody'})[0].findAll('p')
        for p in contentList:
            if len(p.text) > 5 and p.find('img') is None:
                content += '<p>' + p.text.replace('\n', '') + '</p>'
            else:
                pass
    except:
        lw.log_writer('东方财富脚本爬取内容错误')

    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min)

    rst = {'news_link': fullLink.strip(), 'news_title': title.strip(), 'news_source': '东方财富基金资讯',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def main():
    print('天天基金网新闻')
    print()

    # ============= 测试Connection =============
    mydb = connectDB()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news LIMIT 10;')
    print(len(mycursor.fetchall()), ' Connection works')
    print()
    # ============= 测试Connection END =============

    r = requests.get('http://fund.eastmoney.com/a/cjjyw.html')
    soup = BeautifulSoup(r.content, features = 'html.parser')

    # ============== 主页面爬取 ==============
    main_list = soup.find('div', {'class': 'mainCont'}).findAll('ul') # 此处包含页面4个ul
    main_page_item = {} # 用于储存全部该页面的数据
    
    for i in main_list:
        currentUl = i.findAll('a')
        for a in currentUl:
            main_page_item[a.text] = a.get('href')

    print('共', len(main_page_item), '个结果')
    print()
    # ============== 主页面爬取 END ==============

    # ============== 数据库对照 =================
    confirmed_new = []
    for a in main_page_item:
        try:
            sql = 'SELECT news_id, news_title FROM ttd.news WHERE news_title=\'' + str(a) + '\';'
            mycursor.execute(sql)
            compareResult = mycursor.fetchall()
            if len(compareResult) == 0:
                confirmed_new.append(main_page_item[a])
            else:
                pass
        except:
            lw.log_writer('东方财富脚本首页添加新闻错误')
            pass

    lw.log_writer('东方财富脚本本轮新增新闻有' + str(len(confirmed_new)) + '条')
    # ============== 数据库对照 END =================

    # ============== 爬取主代码 =================
    if len(confirmed_new) == 0:
        print('没有发现新增新闻，即将关闭DB链接')
        print()
        mydb.close()
    else:
        for link in confirmed_new:
            sql = 'INSERT INTO ttd.news (news_title, news_source, news_date, news_content, news_link, gov_tag, com_tag) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            rst = parsingContent(link)
            # ======= 标签 - 新增 12.15 ==========
            gov_tag = module_news_govTag.tagGov(mycursor, str(rst['news_title']), str(rst['news_content']))
            com_tag = module_news_comTag.tagCom(mycursor, str(rst['news_title']), str(rst['news_content']))
            # ======= 标签 - 新增 12.15 END ==========
            val = (str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']), gov_tag, com_tag)
            mycursor.execute(sql, val)
            mydb.commit()
            lw.log_writer('东方财富脚本新增' + str(mycursor.rowcount) + '条')
            minorRandomPause()
        
        lw.log_writer('东方财富脚本轮结束')
        mydb.close()
    # ============== 爬取主代码 END =================
    

if __name__ == "__main__":
    main()