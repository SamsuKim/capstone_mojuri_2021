import selenium
import pymysql
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import pykrx
from pykrx import stock
from datetime import datetime
from dateutil.relativedelta import relativedelta

db = pymysql.connect(
    host='13.124.134.15',
    port=3306,
    user='test_user1',
    passwd='12341234',
    db='db_1203',
    charset='utf8')
cursor = db.cursor()

sql = "select r.report_date, r.report_tp, r.company_no from report as r join report_anal as r_a on r.report_no = r_a.report_no and anal_no =4 and report_upside is not null;"

cursor.execute(sql)
result = cursor.fetchall()
date_list = []
tp_list = []
upside_list = []
company_no_list = []

print(result)
data_list = [[0 for i in range(3)] for j in range(len(result))]
for i in range(len(result)):
    data_list[i][0]=result[i][0]
    data_list[i][1]=result[i][1]
    data_list[i][2]=result[i][2]
        
print(data_list)

db.commit()
db.close()




#today = datetime.now()
#b = (today + relativedelta(months=1)).strftime('%Y-%m-%d')
#print(b)

def plus_month(report_date,plus):
    to_date = datetime.strptime(report_date, '%Y-%m-%d')
    #today=datetime.now().strftime('%Y-%m-%d')
    #print('today is '+today)
    #plus_date = ( to_date + relativedelta(months=plus)).strftime('%Y-%m-%d')
    plus_date = to_date + relativedelta(months=plus)
    if plus_date.weekday()==5:
        plus_date1 = (plus_date + relativedelta(days=-1)).strftime('%Y-%m-%d')
    elif plus_date.weekday()==6:
        plus_date1 = (plus_date + relativedelta(days=1)).strftime('%Y-%m-%d')
    else:
        plus_date1 = plus_date.strftime('%Y-%m-%d')
    return plus_date1
   
    #strp가 str에서 date로
    #strf가 date에서 str로


def calculate_future_upside(company_no,date,target_price):
    a = stock.get_market_ohlcv_by_date(
        fromdate=date, todate=date, ticker=company_no)
    b = a.to_numpy()
    future_price = int(b[0][3])

    if(future_price == 0):
        future_upside = 0
    else:
        future_upside = round((target_price - future_price)/future_price * 100, 2)
        print(future_upside)
        #similarity = round((report_upside-future_upside)/report_upside * 100, 2)
    return future_upside        
           




def get_similarity_score(future_upside):
    if future_upside <=0:
        similarity_score = 40
    elif future_upside <= 10:
        similarity_score = 35
    elif future_upside <= 20:
        similarity_score = 30
    elif future_upside <= 30:
        similarity_score = 25
    elif future_upside <= 40:
        similarity_score = 20
    elif future_upside <= 50:
        similarity_score = 16
    elif future_upside <= 75:
        similarity_score = 13
    elif future_upside >75:
        similarity_score = 10
        
    return similarity_score

def multifly_weight_score(i, similarity_score):
    if i == 1:
        report_score = 2 * similarity_score
    elif i == 2:
        report_score = 1.6 * similarity_score
    elif i == 3:
        report_score = 1.4 * similarity_score
    elif i == 4:
        report_score = 1.25 * similarity_score
    elif i == 5:
        report_score = 1.1 * similarity_score
    elif i == 6:
        report_score = similarity_score
        
    return report_score



anal_score_list=[]
score_list = []
for i in range(len(result)):
    report_date = data_list[i][0]
    target_price = data_list[i][1]
    company_no = data_list[i][2]
    for j in range(1, 7):
        date1 = plus_month(report_date, j)
        if date1 == '2021-10-11':
            date1='2021-10-12'
        elif date1 == '2021-10-04':
            date1 = '2021-10-05'
        elif date1 == '2021-09-22':
            date1='2021-09-23'
        elif date1 == '2021-09-20':
            date1='2021-09-17'
        elif date1 == '2021-08-16':
            date1='2021-08-17'
        elif date1 == '2021-09-21':
            date1='2021-09-23'
        
        today = datetime.now().strftime('%Y-%m-%d')
        date2 = date1.replace('-', '')
        print(date1)
        if date1 < today:
            future_upside = calculate_future_upside(
                company_no, date2, target_price)
            print('future_upside is..')
            print(future_upside)
            similarity_score = get_similarity_score(future_upside)
            print(similarity_score)
            report_score = multifly_weight_score(j, similarity_score)
            print('report_score is...')
            print(report_score)
            score_list.append(report_score)
            print('score_list is...')
            print(score_list)
            print(len(score_list))
            avg_report_score = round(sum(score_list)/len(score_list), 2)
            print('avg_report_score is...')
            print(avg_report_score)
            #print('avg_report_score is...')
            #print(avg_report_score)

        else:
            print('time over!')
            break   
          
    #print(score_list)
    #avg_report_score = round(sum(score_list)/len(score_list), 2)
    #print(avg_report_score)
    #anal_score_list.append(avg_report_score)
#anal_score_list.append(avg_report_score)
#print(anal_score_list)
 
        
