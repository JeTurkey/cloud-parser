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
schedule.every().hour.do(parser_eastFund.main) # 东方财富基金资讯
schedule.every().hour.do(parser_caixin.main) # 财新网
schedule.every().hour.do(parser_chinaSecurity.main) # 中国证券报

# ============== 爬虫任务管理 END =================


while True:
    schedule.run_pending()
    time.sleep(1800)