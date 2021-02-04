import schedule
import time
import parser_eastFund
import parser_caixin
import parser_chinaSecurity
import task_comScoreCalculator as task_csc
import task_govScoreCalculator as task_gsc

# ============== 日常计算任务 =================
schedule.every().day.at("23:55").do(task_gsc.main) # 政府计算器
schedule.every().day.at("23:55").do(task_csc.main) # 公司计算器

# ============== 日常计算任务 END =================

# ============== 爬虫任务管理 =================
schedule.every().hour.do(parser_eastFund.main)
schedule.every().hour.do(parser_caixin.main)
schedule.every().hour.do(parser_chinaSecurity.main)

# ============== 爬虫任务管理 END =================


while True:
    schedule.run_pending()
    time.sleep(1800)