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
        title = s.find('h1', {'class': 'dabiaoti'}).text.replace('\n', '')
    except:
        print('title extraction error')

    try:
        contentList = s.find('div', {'id': 'Content'}).findAll('p')
        for p in contentList:
            content += str(p)
    except:
        print('content Extraction error')

    timeFormat = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour)

    rst = {'urlLink': link, 'title': title, 'source': '中国日报经济', 'content': content, 'dateAdded': timeFormat}
    
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
        r = requests.get('http://caijing.chinadaily.com.cn/') # URL 地址
        soup = BeautifulSoup(r.content, features="html.parser")
        results = [] # 储存结果
        # 获取这一页所有title 
        
        # 头版靠右
        topRightLinks = soup.find('div', {'class': 'yaowen'}).findAll('a')[1:]
        for link in topRightLinks:
            if '//' in link.get('href'):
                results.append(link.get('href').replace('//', 'https://'))

        # 跨国公司

        left_liebiao_1 = soup.find('div', {'class': 'left-liebiao'}).findAll('div', {'class': 'busBox1'})
        for link in left_liebiao_1:
            results.append(link.find('a').get('href').replace('//', 'https://'))

        # 产业与公司板块

        left_liebiao_2 = soup.findAll('div', {'class': 'left-liebiao'})[1].findAll('div', {'class': 'busBox1'})
        for link in left_liebiao_2:
            results.append(link.find('a').get('href').replace('//', 'https://'))


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



