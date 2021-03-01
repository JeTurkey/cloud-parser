import schedule
import time
import parser_eastFund
import parser_caixin
import parser_chinaSecurity

# ============== 爬虫任务管理 =================
schedule.every(1.5).hours.do(parser_eastFund.main) # 东方财富基金资讯
schedule.every().hour.do(parser_caixin.main) # 财新网
schedule.every().hour.do(parser_chinaSecurity.main) # 中国证券报

# ============== 爬虫任务管理 END =================

print('爬虫控制中心启动')
while True:
    schedule.run_pending()
    time.sleep(900)