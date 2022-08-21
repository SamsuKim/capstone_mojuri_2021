import pykrx
from pykrx import stock
from datetime import datetime
from dateutil.relativedelta import relativedelta

def find_today_price(company_no,fromdate,todate):
    a = stock.get_market_ohlcv_by_date(fromdate=fromdate, todate=todate, ticker=company_no)
    b = a.to_numpy()
    print(int(b[0][3]))
    #today_price = int(b[0][0])
    #return today_price
    #return today_price

fromdate='20211208'
todate='20211208'
company_no = '139480'
print(find_today_price(company_no,fromdate,todate))
a = datetime.strptime('20211101', "%Y%m%d").date()
print(a.weekday())
b = a + relativedelta(months=1)
print(str(b))
print(b.weekday())
if(b.weekday()==2):
    b = b + relativedelta(days=-1)
print(str(b))
c = str(b).replace('-','')
print(c)


report_date = '2021-06-01'
