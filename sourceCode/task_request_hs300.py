import tushare as ts
import mysql.connector

def main():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                    user='rayshi',
                                    password='Rayshi1994!',
                                    database='ttd',
                                    auth_plugin='mysql_native_password')

        
    print('DB is connected')
    print()

    mycursor = mydb.cursor()

    # 获取历史沪深300 
    hs300 = ts.get_hist_data('hs300')
    hs300['trade_date'] = hs300.index
    for i in range(len(hs300)):
        date = hs300.iloc[i]['trade_date']
        opened = hs300.iloc[i]['open']
        high = hs300.iloc[i]['high']
        close = hs300.iloc[i]['close']
        low = hs300.iloc[i]['low']
        sql = 'INSERT INTO ttd_test.hs300 (trade_date, hs300_open, hs300_high, hs300_close, hs300_low) VALUES (%s, %s, %s, %s, %s)'
        val = (date, opened, high, close, low)
        mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

    print('数据库接口关闭')
    print()
    mydb.close()

if __name__ == "__main__":
    main()