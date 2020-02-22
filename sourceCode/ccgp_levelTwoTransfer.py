import pymongo
import pprint
from pymongo import MongoClient
import sys

client = MongoClient()

db = client.ttd

collection = db.governmentcontractdetails

filename = input('Please enter your file date (Format: YYYYMMDD): ')

systemEnv = input('Please enter your environment Mac / Ubuntu [1/2]: ')

if systemEnv == '1':
    openfile = open('/Users/rayshi/Desktop/cloud-parser/levelTwoResult/ccgp_cleaned' + filename + '.txt', 'r')
elif systemEnv == "2":
    openfile = open('/home/admin/cloud-parser/levelTwoResult/ccgp_cleaned' + filename + '.txt', 'r')
else:
    print('Are u fucking nuts?')
    sys.exit()

for line in openfile.readlines():
    title, pinmu, caigoudanwei, region, bidPublishedDate, judger, totalAmount = line.split(' | ')
