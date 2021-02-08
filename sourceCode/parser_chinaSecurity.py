import mysql.connector
import requests
import time
import datetime
import random
from bs4 import BeautifulSoup
import module_news_comTag
import module_news_govTag
import module_news_topicTag

def minorRandomPause():
    randomTime = random.randint(300, 600)
    print('About to enter minor sleep', randomTime, ' s')
    print()
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
    fullLink = 'http://www.cs.com.cn' + link
    p = requests.get(fullLink)
    s = BeautifulSoup(p.content, features = 'html.parser')

    print('Now parsing', link)
    print()

    title = ''
    content = ''

    # 爬取标题
    try:
        title = s.find('h1').text
    except:
        print('标题获取错误')
        print()

    try:
        contentList = s.find('section').findAll()
        print(contentList)
        for p in contentList:
            if len(p) > 5 and p.find('img') is None:
                content += '<p>' + p.text + '</p>'
            else:
                pass
    except:
        print('内容抓取错误')
        print()

    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min)

    rst = {'news_link': fullLink.strip(), 'news_title': title.strip(), 'news_source': '中国证券报',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def main():
    print('中国证券网')
    print()

    # ============= 测试Connection =============
    mydb = connectDB()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news LIMIT 10;')
    print(len(mycursor.fetchall()), ' Connection works')
    print()
    # ============= 测试Connection END =============

    r = requests.get('http://www.cs.com.cn/')
    soup = BeautifulSoup(r.content, features = 'html.parser')

    # ============== 主页面爬取 ==============
    main_page_item = {}

    top_part = soup.find('div', {'class': 'box410 ch_focus space_l1'}).findAll('li')
    for i in top_part:
        if 'http' not in i.find('a').get('href'):
            main_page_item[i.text] = i.find('a').get('href')

    mid_part = soup.find('div', {'class': 'box_l1'}).findAll('li')
    for i in mid_part:
        if 'http' not in i.find('a').get('href'):
            main_page_item[i.text] = i.find('a').get('href')

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
            print('添加新的新闻错误')
            print()
            pass

    print('本轮新的新闻有', len(confirmed_new), '条')
    # ============== 数据库对照 END =================

    # ============== 爬取主代码 =================
    if len(confirmed_new) == 0:
        print('没有发现新增新闻，即将关闭DB链接')
        print()
        mydb.close()
    else:
        for link in confirmed_new:
            mycursor.execute('SELECT news_id FROM ttd.news ORDER BY news_id DESC LIMIT 1;')
            print('获取最新ID成功')
            print()
            newest_id = int(mycursor.fetchall()[0][0]) + 1
            print('最新ID为', newest_id)
            print()
            sql = 'INSERT INTO ttd.news (news_id, news_title, news_source, news_date, news_content, news_link, gov_tag, com_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            rst = parsingContent(link[1:])
            # ======= 标签 - 新增 12.15 ==========
            gov_tag = module_news_govTag.tagGov(mycursor, str(rst['news_title']), str(rst['news_content']))
            com_tag = module_news_comTag.tagCom(mycursor, str(rst['news_title']), str(rst['news_content']))
            # ======= 标签 - 新增 12.15 END ==========
            val = (newest_id, str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']), gov_tag, com_tag)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, 'row inserted')
            print()
            minorRandomPause()
        
        print('本轮结束, 断开链接')
        mydb.close()
    # ============== 爬取主代码 END =================


if __name__ == "__main__":
    main()
    