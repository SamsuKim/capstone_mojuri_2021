import datetime
from selenium import webdriver
#crawling
import time
import functions as func
# sleep
import pymysql
import pdf2text

URL = 'https://finance.naver.com/research/company_list.naver'
# naver url
# 교보 하나
###################### DATABASE SETTING #####################################################################


host_name = '13.124.134.15'
host_port = 3306
username = 'test_user1'
password = '12341234'
database_name = 'mojuri_test1'

db = pymysql.connect(
    host=host_name,
    port=host_port,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8'
)

print("database connected")
################################# DATABASE SETTING ###########################################################

chrome_options = webdriver.ChromeOptions();

driver = webdriver.Chrome(options=chrome_options, executable_path='chromedriver')
driver.get(url=URL)

table = driver.find_element_by_xpath('//*[@id="contentarea_left"]/div[3]/table[1]/tbody');
trs = table.find_elements_by_tag_name('tr');

for tr in trs:
    tds = tr.find_elements_by_tag_name('td');
    date =''
    name =''
    title = ''
    price = -1
    author = 'inPDF'
    pdfUrl = ''
    sec =''
    if(len(tds)>5):    
        date = tds[4].text
        date = '20'+date[:2]+'-'+date[3:5]+'-'+date[6:8]
        name = tds[0].find_element_by_tag_name('a').text
        title = tds[1].text
        pdfUrl = tds[3].find_element_by_tag_name('a').get_attribute('href')
        sec = tds[2].text;
    if(date!='' and sec!='NICE평가정보'):

        cursor0 = db.cursor()
        sql0 = """SELECT report_title from mojuri_test1.report WHERE report_title = '"""+str(title)+"""';"""
        if cursor0.execute(sql0) :
            print('already_exist')
            continue;
        if sec == '미래에셋증권' or sec == '교보증권' or sec == '하나금융투자': # or sec == '케이프투자증권'
            print(date,name,title,pdfUrl,sec)
            
            authors = []
            tp_anal = pdf2text.getAnalistNTP(pdfUrl,sec)
            print(tp_anal)
            authors.append(tp_anal[1])
            price = tp_anal[0]

            cursor0 = db.cursor()
            sql0 = """SELECT report_title from mojuri_test1.report WHERE report_title = '"""+str(title)+"""';"""

            if cursor0.execute(sql0):
                print('no new report')
                break;

            
            cursor1 = db.cursor()

            sql1 = """INSERT INTO report(report_title,report_date,sec_no,cla_no,report_tp,report_url) VALUES(
            '"""+str(title)+"""',
            '"""+str(date)+"""',
            '"""+str(find_sec_no(sec))+"""',
            '"""+str(1)+"""',
            '"""+str(price)+"""',
            '"""+str(pdfUrl)+"""'
            );"""
            cursor1.execute(sql1)

            cursor2 = db.cursor()
            sql2 = "SELECT last_insert_id();"
            cursor2.execute(sql2)
            result_sql2 = cursor2.fetchone()
            for author in authors:
        
                anal_insert(author)
                anal_no = find_anal_no(author)
                cursor3 = db.cursor();
                
                """
                sql3 = "SELECT anal_no from analyst WHERE anal_name=%s;"
                cursor3.execute(sql3,author)
                result_sql3 = cursor3.fetchone()
                """

                sql4 = "INSERT INTO report_anal(report_no,anal_no) VALUES(%s,%s);"
                cursor3.execute(sql4,(result_sql2[0],anal_no))
        time.sleep(0.5);

driver.quit();
db.commit();

