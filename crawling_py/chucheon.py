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
    db='test_1208',
    charset='utf8')
cursor = db.cursor()

sql = "select r.report_date, r.report_tp,r.report_upside, r.company_no from report as r join report_anal as r_a on r.report_no = r_a.report_no and anal_no =81 and report_upside is not null;"

cursor.execute(sql)
result = cursor.fetchall()
date_list = []
tp_list = []
upside_list = []
company_no_list = []
print(result)
for i in range(len(result)):
    date_list.append(result[i][0])
    tp_list.append(result[i][1])
    upside_list.append(float(result[i][2]))
    company_no_list.append(result[i][3])

        
print(date_list)
print(tp_list)
print(upside_list)
print(company_no_list)

db.commit()
db.close()

today = datetime.now()
b = (today + relativedelta(months=1)).strftime('%Y-%m-%d')
print(b)

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


def calculate_similarity(company_no,date,target_price,report_upside):
    a = stock.get_market_ohlcv_by_date(
        fromdate=date, todate=date, ticker=company_no)
    b = a.to_numpy()
    future_price = int(b[0][3])
    print(future_price)
    if(future_price == 0):
        future_upside = 0
        similarity=0
    else:
        future_upside = round((target_price - future_price)/future_price * 100, 2)
        print(future_upside)
        similarity = round((report_upside-future_upside)/report_upside * 100, 2)
        print(similarity)
    return similarity        
           

#원익피앤이
company_no = '131390'       
report_date = '2021-06-07'
plus = 1
target_price = 30000
report_upside = 47.78

for i in range(1,7):
    date1 = plus_month(report_date,i)
    today = datetime.now().strftime('%Y-%m-%d')
    date2 = date1.replace('-','')
    print(date1)
    print(today)
    print(date2)
    if date1 < today:
        similarity=calculate_similarity(company_no,date2,target_price,report_upside)
        print('similarity is..')
        print(similarity)
    else:
        print('time over!')
        break    
    
a = stock.get_market_ohlcv_by_date(
    fromdate='20210707', todate='20210707', ticker=company_no)
b = a.to_numpy()
future_price = int(b[0][3])
print(future_price)
print((47.78-40.78)/47.78 *100)

def find_today_price(company_no, fromdate, todate):
    a = stock.get_market_ohlcv_by_date(
        fromdate=fromdate, todate=todate, ticker=company_no)
    b = a.to_numpy()
    today_price = int(b[0][0])
    return today_price


def calculate_report_upside(company_no, startdate1, enddate, target_price):
    a = stock.get_market_ohlcv_by_date(
        fromdate=startdate1, todate=enddate, ticker=company_no)
    b = a.to_numpy()
    today_price = int(b[0][3])
    if(today_price == 0):
        upside = 0
    else:
        upside = round((target_price - today_price)/today_price * 100, 2)
        
    return upside
#def calculate_similarity(report_date, report_tp,report_upside):
    
