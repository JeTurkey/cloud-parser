import mysql.connector

def main():
    mydb  = mysql.connector.connect(
        host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
        user='rayshi',
        password='Rayshi1994!',
        database='ttd',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM ttd.news')

    news = mycursor.fetchall()

    d = {}
    rep = []
    for line in news:
        if line[1] in d:
            rep.append(line[0])
        else:
            d[line[1]] = 1

    print('Replicates ', len(rep))

    # 清理news里的结果
    for num in rep:
        sql = "DELETE FROM ttd.news WHERE news_id = " + str(num)

        mycursor.execute(sql)
        
    mydb.commit()

    # 清理gov_news里的结果
    for num in rep:
        sql = "DELETE FROM ttd.gov_news WHERE news_id = " + str(num)

        mycursor.execute(sql)
        
    mydb.commit()  
    print('gov_news duplicates removed')

    # 清理com_news里的结果
    for num in rep:
        sql = "DELETE FROM ttd.com_news WHERE news_id = " + str(num)

        mycursor.execute(sql)

    mydb.commit()
    print('com_news duplicates removed')

    # 清理topic_news里的结果
    for num in rep:
        sql = "DELETE FROM ttd.topic_news WHERE news_id = " + str(num)

        mycursor.execute(sql)

    mydb.commit()
    print("topic_news duplicates removed")

    mydb.close()
    print('remove duplicates finished')

if __name__ == "__main__":
    main()
    