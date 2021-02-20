import mysql.connector
import time
import datetime

# Parameter and Weight

def initialization():
    
    # institution weight
    institutionWeight = {}
    institutionFile = open('/home/admin/sentimentAnalysisTool/referenceList/institutionWeight.txt', 'r')
    for line in institutionFile.readlines():
        ins, weight = line.split(': ')
        institutionWeight[str(ins.strip())] = float(weight.strip())
    institutionFile.close()
        
    # source weight    
    sourceWeight = {}
    sourceFile = open('/home/admin/sentimentAnalysisTool/referenceList/sourceWeight.txt', 'r')
    for line in sourceFile.readlines():
        source, weight = line.split(': ')
        sourceWeight[str(source.strip())] = float(weight.strip())
    sourceFile.close()
    
    # positive sentiment vocabs
    positiveSentimentVocabs = {}
    positiveSentimentVocabsFile = open('/home/admin/sentimentAnalysisTool/referenceList/positiveSentimentVocabs.txt', 'r')
    for line in positiveSentimentVocabsFile.readlines():
        vocab, weight = line.split(': ')
        positiveSentimentVocabs[str(vocab.strip())] = float(weight.strip())
    positiveSentimentVocabsFile.close()
    
    # negative sentiment vocabs
    negativeSentimentVocabs = {}
    negativeSentimentVocabsFile = open('/home/admin/sentimentAnalysisTool/referenceList/negativeSentimentVocabs_v2.txt', 'r')
    for line in negativeSentimentVocabsFile.readlines():
        vocab, weight = line.split(': ')
        negativeSentimentVocabs[str(vocab.strip())] = float(weight.strip())
    negativeSentimentVocabsFile.close()
        
    return institutionWeight, sourceWeight, positiveSentimentVocabs, negativeSentimentVocabs

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                    user='rayshi',
                                    password='Rayshi1994!',
                                    database='ttd',
                                    auth_plugin='mysql_native_password')

        
    print('DB is connected')
    print()
    return mydb

def analysis(data):
    currentScore = 0
    institutionWeight, sourceWeight, positive_words, negative_words = initialization()
    itr = 0
    for i in data:
        sentences = i[4].replace('\u3000', '').split('。')
        for sentence in sentences:
            for sentiment in positive_words.keys():
                if sentiment in sentence:
                    currentScore += (positive_words[sentiment])
                    itr += 1
                    break
            for sentiment in negative_words.keys():
                if sentiment in sentence:
                    currentScore += (negative_words[sentiment])
                    itr += 1
                    break
    if itr == 0:
        itr = 1

    modified_score = currentScore / (itr/(len(sentences)))
    return modified_score

def main():
    mydb = connectDB()
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM ttd_test.hs300 ORDER BY trade_date DESC LIMIT 2')
    t = mycursor.fetchall() # Get latest two result
    prev_score = t[-1][-1] # previous score

    # year = time.localtime().tm_year # year
    # month = time.localtime().tm_mon # month
    # day = time.localtime().tm_mday # day
    d = t[0][0]
    # get all today's news
    mycursor.execute('SELECT * FROM ttd.news WHERE date(news_date)=\'' + str(d) + '\';')
    t = mycursor.fetchall()
    if len(t) > 0:
        s = analysis(t)
        prev_score += s
    else:
        prev_score += 0

    sql = 'UPDATE ttd_test.hs300 SET sentiment_score = %s WHERE trade_date = date(%s)'
    val = (prev_score, d)
    mycursor.execute(sql, val)

    mydb.commit()

    print('score added')

if __name__ == "__main__":
    main()