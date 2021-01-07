import requests
from bs4 import BeautifulSoup
import sys
import mysql.connector
import random
import time
import module_news_govTag
import module_news_comTag

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
    r.encoding = 'GBK'
    s = BeautifulSoup(r.content, features='html.parser')

    print('Now parsing ', link)
    print()

    title = ''
    content = ''

    try:
        title = s.find('div', {'class': 'layout rm_txt cf'}).find('h1').text.replace('\n', '').replace('\r', '')
    except:
        print('title extraction error')
        print()

    try:
        contentList = s.find('div', {'class': 'rm_txt_con cf'}).findAll('p')
        for p in contentList:
            content += str(p).replace('\r', '').replace('\n', '')
    except:
        print('content Extraction error')
        print()

    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '-' + str(t.tm_hour) + '-' + str(t.tm_min)

    rst = {'news_link': link.strip(), 'news_title': title.strip(), 'news_source': '人民日报',
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
            r = requests.get('http://finance.people.com.cn/')
            r.encoding = 'GBK'
            soup = BeautifulSoup(r.content, features="html.parser")
            result = []

            # 版面头条
            try:
                pageMainHeadURL = 'http://finance.people.com.cn/' + soup.find('div', {'class': 'title mt15'}).find('a').get('href')
                result.append(pageMainHeadURL)
            except:
                print('Main page heading extraction error')
                print()

            # 新闻盒子组
            newsBoxList = soup.findAll('div', {'class': 'news_box'})
            for item in newsBoxList:
                sectionHeadURL = 'http://finance.people.com.cn/' + item.find('a').get('href')
                result.append(sectionHeadURL)
                # 找到子目录 news_box
                minorList = item.findAll('a')
                for a in minorList:
                    minorHeadURL = 'http://finance.people.com.cn/' + a.get('href')
                    result.append(minorHeadURL)

            # 切换新闻组
            qiehuanList = soup.findAll('div', {'class': 'headingNews qiehuan1_c'})
            for qiehuan in qiehuanList:
                minorList = qiehuan.findAll('div', {'class': 'hdNews clearfix'})
                for item in minorList:
                    minorHeadURL = item.find('a').get('href')
                    if 'http' not in minorHeadURL:
                        minorHeadURL = 'http://finance.people.com.cn/' + minorHeadURL
                    
                    result.append(minorHeadURL)

            print('This round the result has ', len(result), ' items')
            print()

            # ======== 与数据库对比是否有重复 =========
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
                        sql = 'INSERT INTO ttd.news (news_id, news_title, news_source, news_date, news_content, news_link, gov_tag, com_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                        rst = parsingContent(link)
                        # ======= 政府标签 - 新增 12.15 ==========
                        gov_tag = module_news_govTag.tagGov(mycursor, str(rst['news_title']), str(rst['news_content']))
                        com_tag = module_news_comTag.tagCom(mycursor, str(rst['news_title']), str(rst['news_content']))
                        # ======= 政府标签 - 新增 12.15 END ==========
                        val = (news_id_count, str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']), gov_tag, com_tag)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print(mycursor.rowcount, "record inserted.")
                        print()
                        minorRandomPause()
                    except:
                        print('Getting info error')
                        print()
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

