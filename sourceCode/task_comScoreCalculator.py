import mysql.connector
import time

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
    negativeSentimentVocabsFile = open('/home/admin/sentimentAnalysisTool/referenceList/negativeSentimentVocabs.txt', 'r')
    for line in negativeSentimentVocabsFile.readlines():
        vocab, weight = line.split(': ')
        negativeSentimentVocabs[str(vocab.strip())] = float(weight.strip())
    negativeSentimentVocabsFile.close()
        
    return institutionWeight, sourceWeight, positiveSentimentVocabs, negativeSentimentVocabs

def analysisPosAndNeg(data):
    institutionWeight, sourceWeight, positive_words, negative_words = initialization()
    if len(data) > 0:
        ele = data[0][-2]
        hotWords = ele.split(',') # Enter here
    else:
        print('Pos', 0, 'Neg', 0, 'Neutral', 0, 'Pos_Rate', 0, 'Neg_Rate', 0)
        return 0, 0, 0, 0, 0
    # analysis loop
    pos = 0
    neg = 0
    neutral = 0

    # By Source
    for i in data:
        currentScoreBySource = 0
        sentences = i[7].replace('\u3000', '').split('。')
        for sentence in sentences:
            for word in hotWords:
                if word in sentence:
                    for sentiment in positive_words.keys():
                        if sentiment in sentence:
        #                     currentScoreBySource += (positive_words[sentiment] * sourceWeight[sourceKey])
                            currentScoreBySource += (positive_words[sentiment])
                            break
                    for sentiment in negative_words.keys():
                        if sentiment in sentence:
        #                     currentScoreBySource += (positive_words[sentiment] * sourceWeight[sourceKey])
                            currentScoreBySource += (negative_words[sentiment])
                            break
        if currentScoreBySource > 0:
            pos += 1
        elif currentScoreBySource < 0:
            neg += 1
        else:
            neutral += 1
    
    pos_rate = pos / (pos + neg + neutral)
    neg_rate = neg / (pos + neg + neutral)
    print('Pos', pos, 'Neg', neg, 'Neutral', neutral, 'Pos_Rate', round(pos_rate, 2), 'Neg_Rate', round(neg_rate, 2))
    return pos, neg, neutral, round(pos_rate, 2), round(neg_rate, 2)

def main():
    mydb  = mysql.connector.connect(
        host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
        user='rayshi',
        password='Rayshi1994!',
        database='ttd',
        auth_plugin='mysql_native_password'
    )

    mycursor = mydb.cursor()

    mycursor.execute('SELECT com_id FROM company')

    company_id = mycursor.fetchall()

    print('Start')

    for i in company_id:
        mycursor.execute('SELECT * FROM com_news cn, news n, company c WHERE cn.news_id = n.news_id and c.com_id = cn.com_id and cn.com_id = ' + str(i[0]) + ' and date_sub(curdate(), INTERVAL 30 DAY) <= date(n.news_date);')

        result = mycursor.fetchall()
        
        pos, neg, neutral, pos_rate, neg_rate = analysisPosAndNeg(result)
        
        t = time.localtime()
        news_date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday)
        
        sql = "INSERT INTO ttd.com_score (com_id, record_date, pos, neg, neutral, pos_rate, neg_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (i[0], news_date, pos, neg, neutral, pos_rate, neg_rate)
        
        mycursor.execute(sql, val)
        mydb.commit()

    print('End')
    mydb.close()