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
    lw.log_writer('中央政法委脚本进入休眠' + str(randomTime) + '秒')
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
    t = time.localtime()
    news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_day) + '-' + str(t.tm_hour) + '-' + str(t.tm_min)
    title = ''
    content = ''

    fullLink = 'http://www.chinapeace.gov.cn' + link
    try:
        p = requests.get(fullLink)
        s = BeautifulSoup(p.content, features = 'html.parser')
    except:
        lw.log_writer('中央政法委员会' + fullLink + '失败')
        return {'news_link': fullLink.strip(), 'news_title': title.strip(), 'news_source': '中央政法委', 'news_content': content.strip(), 'news_date': news_date}

    lw.log_writer('中央政法委员会开始爬取' + fullLink)

    try:
        title = s.find('div', {'class': 'title'}).text.replace('\n', '')
    except:
        lw.log_writer('中央政法委员会')

    try:
        contentList = s.findAll('div', {'class': 'content_main'}).find('div', {'id': 'js_content'}).findAll('p')
        for p in contentList:
            if len(p.text) > 5 and p.find('img') is None:
                content += '<p>' + p.text.replace('\n', '') + '</p>'
            else:
                pass
    except:
        lw.log_writer('中央政法委员会获取内容错误')

    rst = {'news_link': fullLink.strip(), 'news_title': title.strip(), 'news_source': '中央政法委',
           'news_content': content.strip(), 'news_date': news_date}

    return rst

def main():
    print('中共中央政法委员会')
    print()

    # ============= 测试Connection =============

    mydb = connectDB()
    mycursor = mydb.cursor()

    # ============= 测试Connection END =============

    try:
        r = requests.get('http://www.chinapeace.gov.cn/chinapeace/c100008/list2020.shtml')
        soup = BeautifulSoup(r.content, features = 'html.parser')

    except:
        return

    # ============== 主页面爬取 ================

    news_list = soup.find('div', {'class': "w1200 bgfff"}).find('div', {'class': 'list_box_left'}).findAll('li')
    news_list_item = {}

    for i in news_list:
        currentLi = i.findAll('a')
        for a in currentLi:
            news_list_item[a.text] = a.get('href')

    print('共', len(news_list_item), '个结果')
    print()
    # ============== 主页面爬取 END ===============

    # ============== 数据库对照 =================
    confirmed_new = []
    for a in news_list_item:
        try:
            sql = 'SELECT news_title, news_link FROM ttd.news WHERE news_title =\'' + str(a) + '\' or news_link = \'' + str(news_list_item[a]) +'\';'
            mycursor.execute(sql)
            compareResult = mycursor.fetchall()
            if len(compareResult) == 0:
                confirmed_new.append(news_list_item[a])
            else:
                pass
        except:
            lw.log_writer('中央政协委员会首页添加新闻错误')
            pass
    
    lw.log_writer('中央政协委员会本轮新增新闻有' + str(len(confirmed_new)) + '条')

    # ============== 数据库对照 END =================

    # ============== 爬取主代码 =================
    if len(confirmed_new) == 0:
        print('没有发现新增新闻,即将关闭DB链接')
        print()
        mydb.close()
    else:
        for link in confirmed_new:
            sql = 'INSERT INTO ttd.news (news_title, news_source, news_date, news_content, news_link, gov_tag, com_tag, topic_tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            rst = parsingContent(link)

            # ======= 标签 - 新增 12.15 ==========
            gov_tag = module_news_govTag.tagGov(mycursor, str(rst['news_title']), str(rst['news_content']))
            com_tag = module_news_comTag.tagCom(mycursor, str(rst['news_title']), str(rst['news_content']))
            topic_tag = module_news_topicTag.tagTopic(mycursor, str(rst['news_title']), str(rst['news_content']))
            # ======= 标签 - 新增 12.15 END ==========
            val = (str(rst['news_title']), str(rst['news_source']), str(rst['news_date']), str(rst['news_content']), str(rst['news_link']), gov_tag, com_tag, topic_tag)
            try:
                mycursor.execute(sql, val)
                mydb.commit()
            except:
                lw.log_writer('中央政协委员会在添加数据时失败')

            lw.log_writer('中央政协新增' + str(mycursor.rowcount) + '条')
            minorRandomPause()

        lw.log_writer('中央政协本轮结束')
        mydb.close()

    # ============== 爬取主代码 END =================

if __name__ == "__main__":
    main()