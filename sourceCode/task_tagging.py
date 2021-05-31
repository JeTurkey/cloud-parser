import schedule
import time
import mysql.connector

def tagGov():
    mydb  = mysql.connector.connect(
        host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
        user='rayshi',
        password='Rayshi1994!',
        database='ttd',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news ORDER BY news_id DESC LIMIT 100;')
    result = mycursor.fetchall()

    sql = 'SELECT * FROM ttd.gov_dept'
    mycursor.execute(sql)
    gov_dept = mycursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    # building gov_news talbe

    for line in result:
        for nick in dept_to_nick:
            for name in dept_to_nick[nick]:
                if name in line[1] or name in line[4]:
                    try:
                        sql = "INSERT IGNORE INTO gov_news (gov_dept_id, news_id, news_date) VALUES (%s, %s, %s)"
                        val = (ind_to_dept[nick], line[0], line[3])
                        mycursor.execute(sql, val)
                        mydb.commit()
                        break
                    except:
                        pass
                    
    print('All done')
    mydb.close()


def tagCom():
    mydb  = mysql.connector.connect(
        host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
        user='rayshi',
        password='Rayshi1994!',
        database='ttd',
        auth_plugin='mysql_native_password'
        )

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news ORDER BY news_id DESC LIMIT 100;')
    result = mycursor.fetchall()

    sql = 'SELECT * FROM ttd.company'
    mycursor.execute(sql)
    gov_dept = mycursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    # building gov_news tabel
    for line in result:
        for nick in dept_to_nick:
            for name in dept_to_nick[nick]:
                if name in line[1] or name in line[4]:
                    try:
                        sql = "INSERT IGNORE INTO ttd.com_news (com_id, news_id, news_date) VALUES (%s, %s, %s)"
                        val = (ind_to_dept[nick], line[0], line[3])
                        mycursor.execute(sql, val)
                        mydb.commit()
                        break
                    except:
                        pass
                    
    print('All done')
    mydb.close()

def tagTopic():
    mydb  = mysql.connector.connect(
        host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
        user='rayshi',
        password='Rayshi1994!',
        database='ttd',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM ttd.news ORDER BY news_id DESC LIMIT 100;')
    result = mycursor.fetchall()

    sql = 'SELECT * FROM ttd.topic'
    mycursor.execute(sql)
    gov_dept = mycursor.fetchall()

    # Turn government department into dict
    ind_to_dept = {}
    dept_to_nick = {}
    for line in gov_dept:
        ind_to_dept[line[1]] = line[0]
        dept_to_nick[line[1]] = line[2].split(",")

    # building gov_news talbe
    for line in result:
        for nick in dept_to_nick:
            for name in dept_to_nick[nick]:
                if name in line[1] or name in line[4]:
                    try:
                        sql = "INSERT IGNORE INTO ttd.topic_news (topic_id, news_id, news_date) VALUES (%s, %s, %s)"
                        val = (ind_to_dept[nick], line[0], line[3])
                        mycursor.execute(sql, val)
                        mydb.commit()
                        break
                    except:
                        pass
                    
    print('All done')
    mydb.close()


def tagging():
    tagGov()
    print('tag Government Done')
    tagCom()
    print('tag Company Done')
    tagTopic()
    print('tag Topic Done')
    # tagGovOnNews()
    # print('Tag Gov On News Done')
    # tagComOnNews()
    # print('Tag Com On News Done')

if __name__ == "__main__":
    tagging()
    