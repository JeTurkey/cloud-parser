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

# ===================  这边每个版本都需要改  Start ==========================

def parsingContent(link):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features="html.parser")
    print('getting ', link)

    title = ''

    content = ''

    try:
        title = s.find('h1', {'class': 'u-title'}).text.replace('\r\n', '').strip()
    except:
        print('title extraction error')

    try:
        contentList = s.find('div', {'class': 'm-l-main'}).find('div', {'id': 'article_inbox'}).findAll('p')
        for p in contentList:
            content += str(p)
    except:
        print('content Extraction error')

    timeFormat = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour)

    rst = {'urlLink': link, 'title': title, 'source': '光明网财经', 'content': content, 'dateAdded': timeFormat}
    
    return rst

# ================== 这边每个版本都需要改  End ===========================

    

def main():
    print('Program initiating ... ...')
    status = True

    # making mongo connection
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['ttd']
    mycol = mydb['news']

    

    while status:
        r = requests.get('https://economy.gmw.cn/') # URL 地址
        soup = BeautifulSoup(r.content, features="html.parser")
        results = [] # 储存结果
        # 获取这一页所有title 
        
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


if __name__ == "__main__":
    main()



