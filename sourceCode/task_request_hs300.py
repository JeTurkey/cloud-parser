import tushare as ts
import mysql.connector

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                    user='rayshi',
                                    password='Rayshi1994!',
                                    database='ttd',
                                    auth_plugin='mysql_native_password')

        
    print('DB is connected')
    print()
    return mydb

def main():

    mydb = connectDB()
    mycursor = mydb.cursor()

    hs300 = ts.get_hist_data('hs300')
    hs300['trade_date'] = hs300.index
    date = hs300.iloc[0]['trade_date']
    opened = hs300.iloc[0]['open']
    high = hs300.iloc[0]['high']
    close = hs300.iloc[0]['close']
    low = hs300.iloc[0]['low']
    sql = 'INSERT INTO ttd_test.hs300 (trade_date, hs300_open, hs300_high, hs300_close, hs300_low) VALUES (%s, %s, %s, %s, %s)'
    val = (date, opened, high, close, low)
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    print('DB Closed')
    print()
    mydb.close()

if __name__ == "__main__":
    main()