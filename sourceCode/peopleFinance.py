import requests
from bs4 import BeautifulSoup
import sys
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


def randomePause(passCount):
    if passCount >= 40:
        randomTime = random.randint(900, 1200)
    else:
        randomTime = random.randint(600, 900)
        
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

    





print('Program initiating ... ...')

status = True
dateOfDay = input('Please enter the date of today in YYYYMMDD: ')
systemEnv = input('Please enter your running environment Mac or Ubuntu [1/2]: ')
urlParsed = []
totalRound = 0
while status:
    passCount = 0
    currentRound_URL = []
    # Getting homepage 
    r = requests.get('http://finance.people.com.cn/')
    soup = BeautifulSoup(r.content, features="html.parser")
    # 获取这一页所有title 
    # 版面头条
    try:
        pageMainHead = soup.find('div', {'class': 'title mt15'}).find('a').text
        pageMainHeadURL = 'http://finance.people.com.cn/' + soup.find('div', {'class': 'title mt15'}).find('a').get('href')
        print('Page head title ', pageMainHead, ' with URL ', pageMainHeadURL)
        currentRound_URL.append(pageMainHeadURL)
    except:
        print('Main page heading extraction error')

    # 新闻盒子组
    newsBoxList = soup.findAll('div', {'class': 'news_box'})
    for item in newsBoxList:
        sectionHead = item.find('h4').text.replace('\n', '')
        sectionHeadURL = 'http://finance.people.com.cn/' + item.find('a').get('href')
        currentRound_URL.append(sectionHeadURL)
        # 找到子目录 news_box
        minorList = item.findAll('a')
        for a in minorList:
            minorHead = a.text
            minorHeadURL = 'http://finance.people.com.cn/' + a.get('href')
            print('News title ', minorHead, ' with href ', minorHeadURL)
            currentRound_URL.append(minorHeadURL)

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
            currentRound_URL.append(minorHeadURL)

    
    # 检测是否在visited 里
    for every in currentRound_URL:
        if every in urlParsed:
            passCount += 1
            pass
        else:
            parsingContent(every, dateOfDay, systemEnv)
            urlParsed.append(every)

    print('The new urlParsed is ', urlParsed, ' with length ', len(urlParsed))
    totalRound += 1
    if totalRound > 20:
        print('Finished')
        break
    
    randomePause(passCount)
    # wait for 10 to 20 mins


