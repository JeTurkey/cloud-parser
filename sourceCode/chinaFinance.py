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

def parsingContent(link, rizi, huanjing):
    page = requests.get(link)
    s = BeautifulSoup(page.content, features="html.parser")

    title = ''
    source = ''
    date = ''
    content = ''

    try:
        title = s.find('div', {'class': 'clearfix w1000_320 text_title'}).find('h1').text.replace('\n', '')
    except:
        print('title extraction error')

    try:
        temp_text = s.find('div', {'class': 'box01'}).find('div', {'class': 'fl'}).text.replace('\xa0', ' ')
        date = temp_text[:temp_text.index(' ')].replace('\n', '')
        source = temp_text[temp_text.index(' '):].replace(' ', '').replace('\n', '')
    except:
        print('date and source extraction error')

    try:
        contentList = s.find('div', {'id': 'rwb_zw'}).findAll('p')
        for p in contentList:
            content += str(p).replace('\n', '')
    except:
        print('content Extraction error')

    rst = title + ' | ' + source + ' | ' + date + ' | ' + content + ' | ' + link + '\n'
    output(rst, rizi, huanjing)
    minorRandomPause()

    

def main():
    print('Program initiating ... ...')
    status = True

    # making mongo connection
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['ttd']
    mycol = mydb['news']

    

    while status:
        r = requests.get('http://finance.china.com.cn/')
        soup = BeautifulSoup(r.content, features="html.parser")
        results = [] # 储存结果
        # 获取这一页所有title 
        
        # 头版靠左
        headLinks = soup.find('div', {'class': 'hot c'}).find('div', {'fl hot-lf'}).findAll('a')
        for link in headLinks:
            if 'http' in link.get('href'):
                results.append(link.get('href'))

        # 金融和资本板块

        f_and_c = soup.find('div', {'class': 'mt20'}).find('div', {'class': 'fl f-list'}).findAll('a')
        for link in f_and_c:
            if len(link.get('href')) > 26:
                results.append(link.get('href'))

        # 产业与公司板块

        i_and_c = soup.find('div', {'class': 'indus mt20'}).find('div', {'class': 'fl f-list pt10'}).findAll('a')
        for link in i_and_c:
            if 'finance' in link.get('href'):
                results.append(link.get('href'))

        for link in results:
            if mycol.count_documents({"urlLink": link}) > 0:
                print('key existed')
                pass
            else:
                new_insert = {'urlLink': link}
                print('New Insert has been made ', new_insert)
                mycol.insert_one(new_insert)

        randomePause()
        # wait for 10 to 20 mins


if __name__ == "__main__":
    main()



