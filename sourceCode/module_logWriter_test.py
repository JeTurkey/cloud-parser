import time

def log_writer(context):
    t = time.localtime()
    year = str(t.tm_year)
    month = str(t.tm_mon)
    day = str(t.tm_mday)
    hr = str(t.tm_hour)
    min = str(t.tm_min)
    sec = str(t.tm_sec)
    fileName = year + '-' + month + '-' + day

    file = open('/Users/rayshi/Desktop/parserOutput/log' + fileName + '.txt', 'a+' )
    specTime = fileName + ' ' + hr + ':' + min + ':' + sec
    file.writelines(specTime + ' : ' + context +'\n')
    file.close()
