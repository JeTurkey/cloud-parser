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

def parsingContent(link):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features="html.parser")
    print('getting ', link)

    title = ''

    content = ''

    try:
        title = s.find('div', {'id': 'the_content'}).find('h1').text.replace('\n', '').replace('\r', '')
    except:
        print('title extraction error')

    try:
        contentList = s.find('div', {'id': 'Main_Content_Val'}).findAll('p')
        for p in contentList:
            content += str(p)
    except:
        print('content Extraction error')

    timeFormat = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour)

    rst = {'urlLink': link, 'title': title, 'source': '财新网', 'content': content, 'dateAdded': timeFormat}
    
    return rst

    

def main():
    print('Program initiating ... ...')
    status = True

    # making mongo connection
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['ttd']
    mycol = mydb['news']

    

    while status:
        r = requests.get('http://www.caixin.com/')
        soup = BeautifulSoup(r.content, features="html.parser")
        results = [] # 储存结果
        # 获取这一页所有title 
        
        # 主页面
        main_list = soup.find('div', {'class': 'news_list'}).findAll('dl')
        for item in main_list:
            results.append(item.find('dd').find('p').find('a').get('href'))



        print('This round the result has ', len(results), ' items')
        
        new_results = []

        for key in results:
            if mycol.count_documents({"urlLink": key}) > 0:
                print(key, ' key existed')
            else:
                new_results.append(key)
                print(key, ' New Key Added')

        
        for key in new_results:
            mycol.insert_one(parsingContent(key))
            minorRandomPause()

if __name__ == "__main__":
    main()



