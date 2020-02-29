import pymongo, pprint
from pymongo import MongoClient

client = MongoClient()

db = client.ttd

gc = db.governmentcontracts

count = 0
dic = {}
for log in gc.find().sort("date", -1):
    if '医疗' in log['title']:
        count += 1
        if log['date'] not in dic.keys():
            dic[log['date']] = 1
        else:
            dic[log['date']] += 1


print(count)
print(dic)

