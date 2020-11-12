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

def parsingContent(link):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features = 'html.parser')

    print('Now parsing', link)
    print()
    
    title = ''
    content = ''

    try: # parsing title
        title = s.find('div', {'id': 'the_content'}).find('h1').text.replace('\n', '').replace('\r', '')
    except:
        print('Title extraction error')
        print()

    try:
        contentList = s.find('div', {'id': 'Main_Content_Val'}).findAll('p')
        for p in contentList:
            content += str(p).replace('\r', '').replace('\n', '')
    except:
        print('Content extraction error')
        print()
    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour)

    rst = {'news_link': link.strip(), 'news_title': title.strip(), 'news_source': '财新网',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def connectDB():
    mydb = mysql.connector.connect(host = 'localhost',
                                   user = 'root', 
                                   password = 'Rayshi1994!',
                                   database = 'ttd')

    
    print('DB is connected')
    print()
    return mydb

def main():
    print('Program initiating ... ...')
    print()

    status = True
    mydb = connectDB()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news LIMIT 10;')
    print(len(mycursor.fetchall()), ' Connection works')
    print()

    while status:
        try:
            r = requests.get('http://www.caixin.com/')
            soup = BeautifulSoup(r.content, features = 'html.parser')
            result = [] # 储存结果
            
            # 主页面
            main_list = soup.find('div', {'class': 'news_list'}).findAll('dl')

            for item in main_list:
                result.append(item.find('dd').find('p').find('a').get('href'))

            print('This round has ', len(result), ' items')
            print()

            
            
            new_result = []
            for link in result:
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
                    except:
                        print('Getting info error')
                        print()
                        status = False
                        break


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

