import requests
from bs4 import BeautifulSoup
import sys
import mysql.connector
import random
import time
import module_news_govTag
import module_news_comTag
import module_logWriter as lw

def majorRandomPause():
    randomTime = random.randint(1800, 3600)
    print('About to enter major sleep', randomTime, ' s')
    print()
    time.sleep(randomTime)

def minorRandomPause():
    randomTime = random.randint(300, 600)
    print('About to enter minor sleep', randomTime, ' s')
    print()
    time.sleep(randomTime)

def parsingContent(link):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features = 'html.parser')

    lw.log_writer('财新网脚本开始爬取' + link)
    
    title = ''
    content = ''

    try: # parsing title
        title = s.find('div', {'id': 'the_content'}).find('h1').text.replace('\n', '').replace('\r', '')
    except:
        lw.log_writer('财新网文章标题获取错误')

    try:
        contentList = s.find('div', {'id': 'Main_Content_Val'}).findAll('p')
        for p in contentList:
            if p.find('img') is None:
                content += str(p).replace('\r', '').replace('\n', '')
            else:
                pass
    except:
        lw.log_writer('财新网文章内容获取错误')

    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min)

    rst = {'news_link': link.strip(), 'news_title': title.strip(), 'news_source': '财新网',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                user='rayshi',
                                password='Rayshi1994!',
                                database='ttd',
                                auth_plugin='mysql_native_password')

    
    print('DB is connected')
    print()
    return mydb

def main():
    print('财新网')
    print()

    # ============= 测试Connection =============
    mydb = connectDB()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news LIMIT 10;')
    # ============= 测试Connection END =============

    r = requests.get('http://www.caixin.com/')
    soup = BeautifulSoup(r.content, features = 'html.parser')

    main_page_item = {} # 用于储存全部该页面数据
    
    # ============= 主页面爬取 =============
    main_list = soup.find('div', {'class': 'news_list'}).findAll('dl')

    for item in main_list:
        a = item.find('dd').find('p').find('a')
        main_page_item[a.text] = a.get('href')

    print('This round has ', len(main_page_item), ' items')
    print()
    # ============= 主页面爬取 END =============

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

    if len(confirmed_new) == 0:
        print('没有发现新增新闻,即将关闭DB链接')
        print()
        mydb.close()
    else:
        for link in confirmed_new:
            try:
                sql = 'INSERT INTO ttd.news (news_title, news_source, news_date, news_content, news_link, gov_tag, com_tag) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                rst = parsingContent(link)
                # ======= 标签 - 新增 12.15 ==========
                gov_tag = module_news_govTag.tagGov(mycursor, str(rst['news_title']), str(rst['news_content']))
                com_tag = module_news_comTag.tagCom(mycursor, str(rst['news_title']), str(rst['news_content']))
                # ======= 标签 - 新增 12.15 END ==========
                val = (str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']), gov_tag, com_tag)
                mycursor.execute(sql, val)
                mydb.commit()
                lw.log_writer('财新网' + str(mycursor.rowcount) + '条')
                minorRandomPause()
            except:
                print('Getting info error')
                print()
                break

    lw.log_writer('财新网脚本本轮结束')
    mydb.close()


        

if __name__ == "__main__":
    main()

