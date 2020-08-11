import requests
from bs4 import BeautifulSoup
import sys
import pymongo
import random, time

def output(str, date, sysEnv):
    if sysEnv is 1 or sysEnv is "1":
        openfile = open('/Users/rayshi/Desktop/cloud-parser/news/peopleFinance' + date + '.txt', 'a+')
        print(str)
        openfile.write(str)
        openfile.close()
    elif sysEnv is 2 or sysEnv is "2":
        openfile = open('/home/admin/cloud-parser/news/peopleFinance' + date + '.txt', 'a+')
        print(str)
        openfile.write(str)
        openfile.close()
    else:
        print('You fuck head, you have entered a invalid system, and you caused the system crash')
        sys.exit()


def randomePause():

    # randomTime = random.randint(6000, 1200)
    randomTime = 6000
        
    print('About to rest ', randomTime, ' s')
    time.sleep(randomTime)

def minorRandomPause():
    randomTime = random.randint(300, 600)
    print('About to rest ', randomTime, ' s')
    time.sleep(randomTime)

def majorRandomPause():
    randomTime = random.randint(1800, 3600)
    print('About to enter major sleep ', randomTime, ' s')
    time.sleep(randomTime)

def parsingContent(link):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features="html.parser")

    title = ''

    content = ''

    try:
        title = s.find('div', {'class': 'clearfix w1000_320 text_title'}).find('h1').text.replace('\n', '')
    except:
        print('title extraction error')

    try:
        contentList = s.find('div', {'id': 'rwb_zw'}).findAll('p')
        for p in contentList:
            content += str(p)
    except:
        print('content Extraction error')

    timeFormat = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour)

    rst = {'urlLink': link, 'title': title, 'source': '人民日报', 'content': content, 'dateAdded': timeFormat}
    
    return rst
    
    

    

def main():
    print('Program initiating ... ...')
    status = True

    # making mongo connection
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['ttd']
    mycol = mydb['news']

    

    while status:
        r = requests.get('http://finance.people.com.cn/')
        soup = BeautifulSoup(r.content, features="html.parser")
        results = dict() # 储存结果
        # 获取这一页所有title 
        # 版面头条
        try:
            pageMainHead = soup.find('div', {'class': 'title mt15'}).find('a').text
            pageMainHeadURL = 'http://finance.people.com.cn/' + soup.find('div', {'class': 'title mt15'}).find('a').get('href')
            print('Page head title ', pageMainHead, ' with URL ', pageMainHeadURL)
            results[str(pageMainHeadURL)] = pageMainHead
        except:
            print('Main page heading extraction error')
        


        # 新闻盒子组
        newsBoxList = soup.findAll('div', {'class': 'news_box'})
        for item in newsBoxList:
            sectionHead = item.find('h4').text.replace('\n', '')
            sectionHeadURL = 'http://finance.people.com.cn/' + item.find('a').get('href')
            results[str(sectionHeadURL)] = sectionHead
            # 找到子目录 news_box
            minorList = item.findAll('a')
            for a in minorList:
                minorHead = a.text
                minorHeadURL = 'http://finance.people.com.cn/' + a.get('href')
                print('News title ', minorHead, ' with href ', minorHeadURL)
                results[str(minorHeadURL)] = minorHead

    # 切换新闻组
        qiehuanList = soup.findAll('div', {'class': 'headingNews qiehuan1_c'})
        for qiehuan in qiehuanList:
            minorList = qiehuan.findAll('div', {'class': 'hdNews clearfix'})
            for item in minorList:
                minorHead = item.find('h5').text
                minorHeadURL = item.find('a').get('href')
                if 'http' not in minorHeadURL:
                    minorHeadURL = 'http://finance.people.com.cn/' + minorHeadURL
                print('News title ', minorHead, ' with href ', minorHeadURL)
                results[str(minorHeadURL)] = minorHead

        print('This round the result has ', len(results), ' items')
        
        new_results = []

        for key in results:
            if mycol.count_documents({"urlLink": key}) > 0:
                print(key, ' key existed')
            else:
                new_results.append(key)
                print(key, ' New Key Added')

        
        if len(new_results) == 0:
            majorRandomPause()
        else:
            for key in new_results:
                mycol.insert_one(parsingContent(key))
                minorRandomPause()


        # wait for 10 to 20 mins


if __name__ == "__main__":
    main()



