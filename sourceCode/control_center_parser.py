import schedule
import time
# import parser_eastFund
import parser_caixin
import parser_chinaSecurity
import parser_chinaPeace
import parser_gwyzc
import parser_xinhua

# ============== 爬虫任务管理 =================
# schedule.every(1.5).hours.do(parser_eastFund.main) # 东方财富基金资讯
schedule.every().hour.do(parser_caixin.main) # 财新网
schedule.every().hour.do(parser_chinaSecurity.main) # 中国证券报
schedule.every().day.at('23:10').do(parser_chinaPeace.main) # 中央政法委
schedule.every(5).hours.do(parser_gwyzc.main) # 国务院政策
schedule.every(4).hours.do(parser_xinhua.main) # 新华网


# ============== 爬虫任务管理 END =================

print('爬虫控制中心启动')
while True:
    schedule.run_pending()
    time.sleep(900)