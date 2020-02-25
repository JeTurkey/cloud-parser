import requests
from bs4 import BeautifulSoup
import time
import random
import sys

def outputUncleaned(string, systemType, date):
    if systemType == "1":
        openfile = open('/Users/rayshi/Desktop/cloud-parser/levelTwoResult/ccgp_uncleaned' + date + '.txt', 'a+')
        openfile.write(str(string) + '\n')
        openfile.close()
    elif systemType == "2":
        openfile = open('/home/admin/cloud-parser/levelTwoResult/ccgp_uncleaned' + date + '.txt', 'a+')
        openfile.write(str(string) + '\n')
        openfile.close

def outputCleaned(string, systemType, date):
    if systemType == "1":
        openfile = open('/Users/rayshi/Desktop/cloud-parser/levelTwoResult/ccgp_cleaned' + date + '.txt', 'a+')
        openfile.write(str(string) + '\n')
        openfile.close()
    elif systemType == "2":
        openfile = open('/home/admin/cloud-parser/levelTwoResult/ccgp_cleaned' + date + '.txt', 'a+')
        openfile.write(str(string) + '\n')
        openfile.close()

# 暂停模块
def randomBreak():
    randomTime = random.randint(300, 400)
    print('About to rest ', randomTime, ' sec')
    time.sleep(randomTime)

confirmFile = ''
fieldate = ''
while confirmFile.upper() != 'Y':
    filedate = input('Please enter the date you wish to extract ')
    print()
    confirmFile = input('You choosed ccgp_ref' + filedate + '.txt, Confirm [Y/N] ')

lineCount = 0
l = []
systemEnvironment = input('Are you in Mac or Ubuntu System? [1/2]? ')
if systemEnvironment == "1":
    for line in open('/Users/rayshi/Desktop/cloud-parser/levelOneResult/ccgp_ref' + filedate + '.txt').readlines( ): lineCount += 1; l.append(line)
    print('Total line is ', lineCount)
elif systemEnvironment == "2":
    for line in open('/home/admin/cloud-parser/levelOneResult/ccgp_ref' + filedate + '.txt').readlines( ): lineCount += 1; l.append(line)
    print('Total line is ', lineCount)
else:
    print('You fucking dumb idiot, program has been terminated')
    sys.exit()



startingPoint = int(input('Please enter a starting point you wish to start [0 for 1st record] '))
parsed = 0
for line in l[startingPoint:]:
    currentURL = line[line.index('http'): -1]
    print(currentURL)


    r = requests.get(currentURL)
    soup = BeautifulSoup(r.content)

    bid_table = soup.find('div', {'class': 'table'})
    parsed += 1

    rst = ''

    for items in bid_table.find_all('tr'):

        temp_list = items.find_all('td')
        if len(temp_list) > 1:
            rst += temp_list[0].text + ' : ' + temp_list[1].text + ' | '
    
    try:
        detail = soup.find('div', {'class': 'vF_detail_content_container'}).text
        detail_text = detail.replace('\n', '').replace('\xa0', '')
    except:
        print(' Cleaning text issue ')

    rst += '详细内容 : ' + detail_text + ' | '

    # Cheking if detail have table tag
    try:
        iftabletag = soup.find('div', {'class': 'vF_detail_content_container'}).find('table')
        if len(iftabletag) >= 1:
            tabletag = 'Yes'
        else:
            tabletag = 'No'
        rst += 'Table Tag : ' + tabletag + ' | '
    except:
        print('Error in finding table tag')

    # Appending url at the end
    rst += currentURL
    print(rst)
    if rst.count('详情') >= 3:
        outputUncleaned(rst, systemEnvironment, filedate)
    else:
        outputCleaned(rst, systemEnvironment, filedate)

    randomBreak()
    print('已完成 ', parsed, ' 条')
    

        