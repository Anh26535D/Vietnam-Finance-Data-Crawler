import pandas as pd
import sys
import math
sys.path.append(r'A:\DataVietNam')
sys.path.append(r'A:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL_CONFIG import *
from base.Setup import *
from Flow.utils import *
pd.options.mode.chained_assignment = None
QUARTER_KEY = "1_2023"
print("Path get data: ",FU.PATH_MAIN_CURRENT)
PRICE = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE.json").rename(columns={"Day":"Time"})
# print(PRICE)
DIVIDEND = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/DIVIDEND.xlsx")
# print(DIVIDEND)
FINANCIAL = pd.read_csv(f"{PATH_DISTILLATION_VIETNAM_ALLREAL}/{QUARTER_KEY}.csv")
# print(FINANCIAL)

def getClose(symbol,start,end,Close):
    end += datetime.timedelta(days=3)

    # Nếu ngày ghép giá ko phải đúng lịch thì chỉnh sửa các này
    end = datetime.datetime(end.year,end.month,end.day-3)
    end_end = datetime.datetime(end.year,end.month,end.day+25)
    end,end_end = end.strftime("%Y-%m-%d"),end_end.strftime("%Y-%m-%d")
    print(end,end_end,33333)

    df = Close[(Close['Time'] == start) & (Close['Symbol'] == symbol)].reset_index(drop=False)
    try:
        buy = df["Price"][0]
        if buy == 0:
            buy = df["prePrice"][0]
    except KeyError:
        buy = 0
    df = Close[(Close['Time'] >=end)& (Close['Time'] <= end_end) & (Close['Symbol'] == symbol)].sort_values(by=['Time']).reset_index(drop=False)
    try:
        while math.isnan(df["Price"][0]) or df["Price"][0] == 0:
            df = df.drop(df.index[0])
            df = df.reset_index(drop=True)
        sell = df["Price"].loc[0]
    except:
        print(symbol)
        print(Close)
        sell = -1

    return buy/1000,sell/1000

def getDividend(symbol):
    try:
        dividend = DIVIDEND[(DIVIDEND['Symbol'] == symbol)].reset_index()
    except FileNotFoundError:
        dividend = pd.DataFrame()
    except:
        dividend = pd.DataFrame()
    return dividend

def getSale(start,time,symbol,Close,dividend):
    # print(time,symbol)
    v,end = CoverTime(time,year=TYPE_TIME)
    buy,value = getClose(symbol,start,end,Close)
    sum = 0
    cp=1
    if dividend.empty:
        return buy,value*cp+sum
    df = dividend[(dividend['Time'] >=start) & (dividend['Time'] <=end.strftime("%Y-%m-%d"))].reset_index()
    for i in df.index:
        if df["Money"][i] != "NAN":
            tyle = df["Money"][i]
            sum = sum + cp*10*eval(tyle)
        if df["Stock"][i] != "NAN":
            tyle = df["Stock"][i]
            cp = cp*1/eval(tyle)+cp
    return buy,value*cp+sum
# getSale("2023-05-06","2023-08-01","AAA",PRICE,DIVIDEND)
# print(getSale("2023-05-06","2023-08-01","AAA",PRICE,DIVIDEND))
# getSale(FINANCIAL["Date_Buy"].iloc[i],FINANCIAL["Time_Investment_Number"].iloc[i],FINANCIAL['Symbol'].iloc[i],Close,dividend)
FILE_TOTAL = FINANCIAL
sym = ""
for i in FILE_TOTAL.index:
    if sym != FILE_TOTAL['Symbol'].iloc[i]:
        sym = FILE_TOTAL['Symbol'].iloc[i]
        Close = PRICE[PRICE['Symbol'] == sym].reset_index(drop=True)
        dividend = getDividend(sym)
        # print(FILE_TOTAL["Date_Buy"].iloc[i],FILE_TOTAL["Time_Investment_Number"].iloc[i],FILE_TOTAL['Symbol'].iloc[i],99999)
        # # ,Close,dividend,
        m,b = getSale(FILE_TOTAL["Date_Buy"].iloc[i],FILE_TOTAL["Time_Investment_Number"].iloc[i],FILE_TOTAL['Symbol'].iloc[i],Close,dividend)
        FILE_TOTAL["SELL"][i] = b
        # print(m,b)
FILE_TOTAL['PROFIT'] = FILE_TOTAL['SELL']/FILE_TOTAL['BUY']
# print(FILE_TOTAL)
FILE_TOTAL.to_csv(f"{FU.PATH_MAIN_CURRENT}/FILE_TOTAL.csv",index=False)