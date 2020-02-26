import requests
import time
import random
import sys
from bs4 import BeautifulSoup
import os.path

# Getting all the inputs

confirmStartingDate = ""
while confirmStartingDate.upper() != "Y":
    startYear = input("Please enter starting year format: YYYY ")
    startMonth = input("Please enter starting month format: Jan=1 Dec=12 ")
    startDay = input("Please enter starting day format: 1st=1 10th=10 ")
    confirmStartingDate = input("Please confirm starting date " + str(startYear) + ' / ' + str(startMonth) + ' / ' + str(startDay) + ' ? [Y/N] ')

confirmEndingDate = ""
while confirmEndingDate.upper() != "Y":
    endYear = input("Please enter ending year format:YYYY ")
    endMonth = input("Please enter ending month format: Jan=1 Dec=12 ")
    endDay = input("Please enter ending day format: 1st=1 10th=10 ")
    confirmEndingDate = input("Please confirm the ending date " + str(endYear) + ' / ' + str(endMonth) + ' / ' + str(endDay) + ' ? [Y/N] ')

print("About to begin " + str(startYear) + ' / ' + str(startMonth) + ' / ' + str(startDay) + ' -- ' + str(endYear) + ' / ' + str(endMonth) + ' / ' + str(endDay) + ' records' )
print()

filename = str(endYear)
if int(endMonth) < 10:
    filename += '0' + str(endMonth)
else:
    filename += str(endMonth)
if int(endDay) < 10:
    filename += '0' + str(endDay)
else:
    filename += str(endDay)

print('File has been saved as ccgp_ref', filename, '.txt')
print()

# 输出口模块
def output(string, filename):
    # openfile = open('/Users/rayshi/Desktop/cloud-parser/levelOneResult/ccgp_ref' + filename + '.txt', 'a+')
    openfile = open('/home/admin/cloud-parser/levelOneResult/ccgp_ref' + filename + '.txt', 'a+')
    openfile.write(str(string) + '\n')
    openfile.close()

# 暂停模块
def randomBreak():
    randomTime = random.randint(240, 360)
    print('About to rest ', randomTime, ' s')
    time.sleep(randomTime)

# 需要模块获得page总数

# request website
page_index = int(input('Please enter the starting page index: '))
print()
r = requests.get('http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=' + str(page_index) + '&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + str(startYear) + '%3A' + str(startMonth) + '%3A' + str(startDay) + '&end_time=' + str(endYear) + '%3A' + str(endMonth) + '%3A' + str(endDay) + '&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=')
# render page data
soup = BeautifulSoup(r.content)
# get entry and page count first and save it
entryCount = soup.findAll('div', {'class':'vT_z'})[3].findAll('div')[0].findAll('span')[1].text
temp = soup.findAll('div', {'class': 'vT_z'})[3].findAll('div')[0].find('p', {'class': 'pager'}).find('script').text
init = temp.index('size: ') + 6
pageCount = int(temp[init: init+temp[init:].index(',')])

print(startYear,' / ', startMonth,' / ', startDay, ' -- ', endYear, ' / ', endMonth, ' / ', endDay, ' has total ', entryCount, ' records，total ', pageCount, ' pages')


while int(page_index) <= pageCount:
    # 提醒部分
    print('Currently in  ', page_index)
    bid_result = soup.find('ul', {'class': 'vT-srch-result-list-bid'})
    bid_list = bid_result.find_all('li')
    print('Total ', len(bid_list), ' records in the page')
    for items in bid_list:
        # 初始化所有变量
        title = ''
        wholeString = ''
        date = ''
        caigouren = ''
        dailijigou = ''
        province = ''
        purchase_info = ''
        url = ''
        rst = ''

        # 爬取
        # URL Part
        try:
            url = items.contents[1].get('href')
        except:
            print('Cannot extract URL')
            pass
    # 标题
        try:
            title = items.contents[1].text.replace(" ", "").replace("\r", "").replace("\n", "")
        except:
            print('Title not found')
            pass
    # 剩余信息来自于whole string，所以需要先读取whole string
        try:
            wholeString = items.contents[5].text.replace(" ", "").replace("\r", "").replace("\n", "")
        except:
            print('wholeString wrong')
            pass

    # 截取 日期 部分
        date = wholeString[:wholeString.index("|")][:10]
        # 更新 wholeString
        wholeString = wholeString[wholeString.index("|") + 1:]
        
        # 截取 采购人 部分
        caigouren = wholeString[:wholeString.index("|")][4:]
        # 更新 wholeString
        wholeString = wholeString[wholeString.index("|") + 1:]

        # 截取 代理机构 部分
        dailijigou = wholeString[:wholeString.index("|")][5:]
        # 更新 wholeString
        wholeString = wholeString[wholeString.index("|") + 1:]

        # 截取 省份 部分
        province = wholeString[:wholeString.index("|")]
        # 更新 wholeString
        wholeString = wholeString[wholeString.index("|") + 1:]
    

        # 截取 采购内容 部分 
        if len(str(items.find('img'))) > 5:
            purchase_info = 'PPP'
        else:
            purchase_info = wholeString
        print('标题 ', title, ' 日期 ', date, ' 采购人 ', caigouren, ' 代理机构 ', dailijigou, ' 省份 ', province, ' 采购内容 ', purchase_info, ' 链接 ', url)
        rst = title + ' | ' + date + ' | ' + caigouren + ' | ' + dailijigou + ' | ' + province + ' | ' + purchase_info + ' | ' + url
        output(rst, filename)    
    
    # page_index 递增
    page_index += 1
    # 最终页终止条件
    if page_index > pageCount:
        print('All finished')
        break
    # 读取新的一页
    r = requests.get('http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=' + str(page_index) + '&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + str(startYear) + '%3A' + str(startMonth) + '%3A' + str(startDay) + '&end_time=' + str(endYear) + '%3A' + str(endMonth) + '%3A' + str(endDay) + '&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=')
    soup = BeautifulSoup(r.content)
    # 暂停
    randomBreak()


