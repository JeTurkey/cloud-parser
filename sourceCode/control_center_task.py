import schedule
import time
import task_tagging
import task_comScoreCalculator as task_csc
import task_govScoreCalculator as task_gsc
import task_request_hs300 as task_hs300
import task_sentimentIndexCalculator as task_sic

# ============== 日常计算任务 =================
schedule.every().day.at("23:30").do(task_gsc.main) # 政府计算器
schedule.every().day.at("23:30").do(task_csc.main) # 公司计算器

schedule.every().hour.do(task_tagging.tagging) # 在bridge打标签

schedule.every().monday.at("22:30").do(task_sic.main) # 计算当天分数 - 周一
schedule.every().tuesday.at("22:30").do(task_sic.main) # 计算当天分数 - 周二
schedule.every().wednesday.at("22:30").do(task_sic.main) # 计算当天分数 - 周三
schedule.every().thursday.at("22:30").do(task_sic.main) # 计算当天分数 - 周四
schedule.every().friday.at("22:30").do(task_sic.main) # 计算当天分数 - 周五
# ============== 日常计算任务 END =================

# ============== 日常获取数据任务 =================
schedule.every().monday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周一
schedule.every().tuesday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周二
schedule.every().wednesday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周三
schedule.every().thursday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周四
schedule.every().friday.at("22:00").do(task_hs300.main) # 获取沪深300数据 - 周五

# ============== 日常获取数据任务 END =================

while True:
    schedule.run_pending()
    time.sleep(900)