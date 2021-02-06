import schedule
import time
import parser_eastFund
import parser_caixin
import parser_chinaSecurity
import task_comScoreCalculator as task_csc
import task_govScoreCalculator as task_gsc
import task_request_hs300 as task_hs300

# ============== 日常计算任务 =================
schedule.every().day.at("23:55").do(task_gsc.main) # 政府计算器
schedule.every().day.at("23:55").do(task_csc.main) # 公司计算器

# ============== 日常计算任务 END =================

# ============== 爬虫任务管理 =================
schedule.every().hour.do(parser_eastFund.main) # 东方财富基金资讯
schedule.every().hour.do(parser_caixin.main) # 财新网
schedule.every().hour.do(parser_chinaSecurity.main) # 中国证券报

# ============== 爬虫任务管理 END =================

# ============== 日常获取数据任务 =================
schedule.every().monday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周一
schedule.every().tuesday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周二
schedule.every().wednesday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周三
schedule.every().thursday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周四
schedule.every().friday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周五


# ============== 日常获取数据任务 END =================


while True:
    schedule.run_pending()
    time.sleep(1800)