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

def connectDB():
    mydb = mysql.connector.connect(host='rm-bp11g1acc24v9f69t1o.mysql.rds.aliyuncs.com',
                                    user='rayshi',
                                    password='Rayshi1994!',
                                    database='ttd',
                                    auth_plugin='mysql_native_password')

        
    print('DB is connected')
    print()
    return mydb

def sentimentAnalysis():
    mydb = connectDB()
    mycursor = mydb.cursor()
    # get all news
    mycursor.execute('SELECT * from ttd.news')
    news_result = mycursor.fetchall()

    mycursor.execute('SELECT * from ttd_test.hs300')
    hs300_result = mycursor.fetchall()

    date = [d[0] for d in hs300_result]
        