import requests
import time
import random
import sys
from bs4 import BeautifulSoup
import os.path

# Getting all the inputs

confirmStartingDate = ""
while confirmStartingDate.upper() != "Y":
    startYear = input("请输入起始搜索年份 格式:YYYY ")
    startMonth = input("请输入起始搜索月份 格式:1月=1 12月=12 ")
    startDay = input("请输入起始搜索日期 格式:1号=1 10号=10 ")
    confirmStartingDate = input("请确认起始搜索日期为 " + str(startYear) + ' 年 ' + str(startMonth) + ' 月 ' + str(startDay) + ' 日? [Y/N] ')

confirmEndingDate = ""
while confirmEndingDate.upper() != "Y":
    endYear = input("请输入结束搜索年份 格式:YYYY ")
    endMonth = input("请输入结束搜索月份 格式:1月=1 12月=12 ")
    endDay = input("请输入结束日期 格式:1号=1 10号=10 ")
    confirmEndingDate = input("请确认起始搜索日期为 " + str(endYear) + ' 年 ' + str(endMonth) + ' 月 ' + str(endDay) + ' 日? [Y/N] ')

print("将开始爬取 " + str(startYear) + ' 年 ' + str(startMonth) + ' 月 ' + str(startDay) + ' 日至 ' + str(endYear) + ' 年 ' + str(endMonth) + ' 月 ' + str(endDay) + ' 日的记录' )
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

print('储存文件名为 ccgp_levelOne', filename, '.txt')

# 输出口模块
def output(string, filename):
    openfile = open('/home/admin/cloud-parser/levelOneResult/ccgp_ref' + filename + '.txt', 'a+')
    openfile.write(str(string) + '\n')
    openfile.close()

# 暂停模块
def randomBreak():
    randomTime = random.randint(60, 120)
    print('即将休眠 ', randomTime, ' 秒')
    time.sleep(randomTime)

# 需要模块获得page总数

# request website
page_index = input('请输入开始页数')
r = requests.get('http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=' + str(page_index) + '&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + str(startYear) + '%3A' + str(startMonth) + '%3A' + str(startDay) + '&end_time=' + str(endYear) + '%3A' + str(endMonth) + '%3A' + str(endDay) + '&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=')
# render page data
soup = BeautifulSoup(r.content)
# get entry and page count first and save it
entryCount = soup.findAll('div', {'class':'vT_z'})[3].findAll('div')[0].findAll('span')[1].text
temp = soup.findAll('div', {'class': 'vT_z'})[3].findAll('div')[0].find('p', {'class': 'pager'}).find('script').text
init = temp.index('size: ') + 6
pageCount = int(temp[init: init+temp[init:].index(',')])

print(startYear,' 年 ', startMonth,' 月 ', startDay, ' 日至 ', endYear, ' 年 ', endMonth, ' 月 ', endDay, ' 日共有 ', entryCount, ' 条记录，共有 ', pageCount, ' 页结果')


while page_index <= pageCount:
    # 提醒部分
    print('当前页面 ', page_index)
    bid_result = soup.find('ul', {'class': 'vT-srch-result-list-bid'})
    bid_list = bid_result.find_all('li')
    print('本页共 ', len(bid_list), ' 条数据')
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
            print('无法获得URL')
            pass
    # 标题
        try:
            title = items.contents[1].text.replace(" ", "").replace("\r", "").replace("\n", "")
        except:
            print('没有找到项目标题')
            pass
    # 剩余信息来自于whole string，所以需要先读取whole string
        try:
            wholeString = items.contents[5].text.replace(" ", "").replace("\r", "").replace("\n", "")
        except:
            print('wholeString部分出错')
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
        print('已完成全部采集 终止')
        break
    # 读取新的一页
    r = requests.get('http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=' + str(page_index) + '&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=7&dbselect=bidx&kw=&start_time=' + str(startYear) + '%3A' + str(startMonth) + '%3A' + str(startDay) + '&end_time=' + str(endYear) + '%3A' + str(endMonth) + '%3A' + str(endDay) + '&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName=')
    soup = BeautifulSoup(r.content)
    # 暂停
    randomBreak()


