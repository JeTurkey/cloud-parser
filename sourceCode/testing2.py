import modeule_news_govTag
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
print(modeule_news_govTag.tagGov(mycursor, '阿里巴巴哟哦i我饥饿佛i我', '蚂蚁金服jslkdjflksjfoii'))
print('DB close')
mydb.close()

# mydb = testing.connectDB()
# print(testing.tagCom(mydb, 'sjflsdkjfl'))
# mydb.close()