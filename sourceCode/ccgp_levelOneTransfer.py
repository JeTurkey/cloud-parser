import pymongo
import pprint
from pymongo import MongoClient


# Initiate a mongod client
client = MongoClient()

# connect to database
db = client.ttd
# connect to collections
collection = db.governmentcontracts


filename = input('Please enter your file date (Format: YYYYMMDD): ')
openfile = open('/home/admin/levelOneResult/ccgp_ref' + filename + '.txt', 'r')

for line in openfile.readlines():
    title, date, subject, intermediate, location, purchaseInfo, url = line.split(' | ')
    print(' 标题 ', title)
    print(' 日期 ', date)
    print(' 采购方 ', subject)
    if intermediate.index("中标公告") > 0:
        intermediate = intermediate[:intermediate.index("中标公告")]
    print(' 代理商 ', intermediate)
    print(' 地址 ', location)
    if len(purchaseInfo) == 0:
        purchaseInfo = "未知"
        print(' 购买内容 ', purchaseInfo)
    else:
        print(' 购买内容 ', purchaseInfo)
    print(' 链接 ', url)

    record = {"title": title,
              "date": date,
              "caigouren": subject,
              "dailishang": intermediate,
              "location": location,
              "caigouneirong": purchaseInfo,
              "link": url}

    
    collection.insert_one(record)