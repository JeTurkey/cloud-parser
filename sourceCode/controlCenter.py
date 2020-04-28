import datetime
import threading

def func():
    print("init threading timer")
    #如果需要循环调用，就要添加以下方法
    timer = threading.Timer(86400, func)
    timer.start()