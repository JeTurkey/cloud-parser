import mysql.connector
import time
import datetime

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                    user='rayshi',
                                    password='Rayshi1994!',
                                    database='ttd',
                                    auth_plugin='mysql_native_password')

        
    print('DB is connected')
    print()
    return mydb

def countingTopic(local_news, tag, record_date, db, cursor):
    ind_to_topic = {}
    topic_to_nick = {}
    for line in tag:
        ind_to_topic[line[1]] = line[0]
        topic_to_nick[line[1]] = line[2].split(",")
    topic_count = ind_to_topic
    
    for i in topic_count: # reset to zero
        topic_count[i] = 0
    
    
    for news in local_news:
        for nick in topic_to_nick:
            for name in topic_to_nick[str(nick)]:
                if str(name) in str(news[1]) or str(name) in str(news[4]):
                    topic_count[nick] += 1
                    break

    for i in topic_count:
        sql = 'INSERT IGNORE INTO ttd.topic_trend (topic_id, topic_name, topic_count, record_date) VALUES (%s, %s, %s, %s);'
        val = (str(ind_to_topic[i]), str(i), str(topic_count[i]), record_date)
        cursor.execute(sql, val)
    db.commit()
    return topic_count

def main():
    mydb = connectDB()
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM ttd.topic;')
    topic_tags = mycursor.fetchall()

    year = time.localtime().tm_year
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    mycursor.execute('SELECT * FROM ttd.news WHERE date(news_date)=\'' + str(year) + '-' + str(month) + '-' + str(day) + '\';')
    daily_news = mycursor.fetchall()

    countingTopic(daily_news, topic_tags, str(year) + '-' + str(month) + '-' + str(day), mydb, mycursor)    

if __name__ == "__main__":
    main()