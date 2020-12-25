import requests
from bs4 import BeautifulSoup
import sys
import mysql.connector
import random
import time

def tagCom(connection, content):
    mycursor = connection.cursor()
    # Grab all untagged row
    mycursor.execute('SELECT * FROM ttd.company')
    result = mycursor.fetchall()
    return result


def connectDB():
    mydb  = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Rayshi1994!',
        database='ttd'
    )

    
    print('DB is connected')
    print()
    return mydb

mydb = connectDB()
tagCom(mydb, 'lkjsljfkd')
print('DB close')
mydb.close()