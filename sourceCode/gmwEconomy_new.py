import requests
from bs4 import BeautifulSoup
import sys
import mysql.connector
import random
import time

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
    r = requests.get(link)
    s = BeautifulSoup(r.content, features = 'html.parser')
    
    print('Getting ', link)
    print()

    title = ''
    content = ''

    try:
        title = s.find('h1', {'class': 'u-title'}).text.replace('\r\n', '').strip()
    except:
        print('title extraction error')
        print()

    try:
        contentList = s.find('div', {'class': 'm-l-main'}).find('div', {'id': 'article_inbox'}).findAll('p')
        for p in contentList:
            content += str(p).replace('\r', '').replace('\n', '')
    except:
        print('content Extraction error')
        print()

    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour)

    rst = {'news_link': link.strip(), 'news_title': title.strip(), 'news_source': '光明网财经',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def main():
    print('Program initiating ... ...')
    print()

    status = True


    while status:
        try:
            # ============= 测试Connection =============
            mydb = connectDB()
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM ttd.news LIMIT 10;')
            print(len(mycursor.fetchall()), ' Connection works')
            print()
            # ============= 测试Connection END =============
            r = requests.get('https://economy.gmw.cn/') # URL 地址
            soup = BeautifulSoup(r.content, features="html.parser")
            results = [] # 储存结果

            # 头版靠左
            topLeftLinks = soup.find('div', {'class': 'part1'}).find('ul').findAll('li')
            for link in topLeftLinks:
                if 'http' not in link.find('a').get('href'):
                    results.append('https://economy.gmw.cn/' + link.find('a').get('href'))
                else:
                    results.append(link.find('a').get('href'))

            # 要闻

            yaowen = soup.find('div', {'class': 'part2 inner1000 clearfix'}).find('ul', {'class': 'arc_list_t1 clearfix'}).findAll('li')
            for link in yaowen:
                if 'http' not in link.find('a').get('href'):
                    results.append('https://economy.gmw.cn/' + link.find('a').get('href'))
                else:
                    results.append(link.find('a').get('href'))

            # 产经板块

            chanjing = soup.find('ul', {'class': 'arc_pic_list'}).findAll('li')
            for link in chanjing:
                if 'http' not in link.find('a').get('href'):
                    results.append('https://economy.gmw.cn/' + link.find('a').get('href'))
                else:
                    results.append(link.find('a').get('href'))


            print('This round the result has ', len(results), ' items')
            print()

            # ======== 与数据库对比是否有重复 =========
            new_result = []
            for link in results:
                try:
                    sql = 'SELECT news_id FROM ttd.news WHERE news_link=\'' + str(link).strip() + '\';'
                    mycursor.execute(sql)
                    news_link = mycursor.fetchall()
                    if len(news_link) < 1:
                        print('New link found', link)
                        print()
                        new_result.append(link)
                    else:
                        print(link, ' Existed')
                        print()
                except:
                    print('Adding new item error')
                    print()
                    status = False
                    break

            print('This round has ', len(new_result), ' new items')
            print()

            # ======== 与数据库对比是否有重复 END =========

            # ======== 插入新数据 =========
            if len(new_result) == 0:
                majorRandomPause()
            else:
                for link in new_result:
                    try:
                        mycursor.execute('SELECT news_id FROM ttd.news ORDER BY news_id DESC LIMIT 1;')
                        print('Execute Successfully')
                        news_id_count = mycursor.fetchall()[0][0] + 1
                        print(news_id_count)
                        sql = 'INSERT INTO ttd.news VALUES (%s, %s, %s, %s, %s, %s)'
                        rst = parsingContent(link)
                        val = (news_id_count, str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']))
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, "record inserted.")
                        print()
                        minorRandomPause()
                    except:
                        print('Getting info error')
                        print()
                        status = False
                        break

                # ======== 插入新数据 END =========
            print('This round has end, close connection')
            print()
            mydb.close()

        except:
            print('An error happend, minor stop')
            print()
            mydb.close()
            minorRandomPause()
            print('Reconnecting')
            print()
            mydb = connectDB()
            mycursor = mydb.cursor()

if __name__ == "__main__":
    main()
