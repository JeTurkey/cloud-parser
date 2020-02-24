import pymongo
import pprint
from pymongo import MongoClient


client = MongoClient('mongodb://root:Rayshi1994!@47.94.170.122:27017/')


db = client.test

collection = db.test


pprint.pprint(collection.find_one())