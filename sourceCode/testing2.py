
import mysql.connector

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
mycursor = mydb.cursor()
sql = 'SELECT news_id, news_title FROM ttd.news WHERE news_title=\''+str('lksdjfoiwe') + '\';'
mycursor.execute(sql)
rst = mycursor.fetchall()
print('返回长度',len(rst))
mydb.close()

# mydb = testing.connectDB()
# print(testing.tagCom(mydb, 'sjflsdkjfl'))
# mydb.close()