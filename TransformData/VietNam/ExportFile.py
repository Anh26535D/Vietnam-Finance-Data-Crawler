import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL import *
from base.Setup import *
from Flow.ulis import *

PRICE = pd.read_json(f"{FU.PATH_MAIN_CURRENT}/PRICE.json").rename(columns={"Date":"Time"})
# PRICE["Time"]=PRICE["Time"].astype(str)
DIVIDEND = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/DIVIDEND.xlsx")
FINANCIAL = pd.read_excel(f"{FU.PATH_MAIN_CURRENT}/FINANCAIL_{QUARTER_KEY.replace('/','_')}.xlsx")
INFOR = List_Symbol[["Mã CK▲","Sàn"]].rename(columns={"Mã CK▲":"Symbol",
                                                    "Sàn":"Exchange"})
FILE_TOTAL = pd.merge(FINANCIAL,INFOR,on=["Symbol"],how="outer")
FILE_TOTAL["Time"] = [f'{QUARTER_KEY.split("/")[1]}/{QUARTER_KEY.split("/")[0]}' for i in FILE_TOTAL.index]
FILE_TOTAL["Time_Investment_Number"] = FILE_TOTAL["Time"].apply(lambda x: int(x.split("/")[1]) + (int(x.split("/")[0])-2000)*4)

def count_company(dt):
    count = 0
    for i in COMPANY_ACTIVE:
        if i in dt["Symbol"].values:
            count +=1
    return count

def checkTime(number):
    start,e = CoverTime(number,TYPE_TIME)
    df = pd.DataFrame()
    temp = FILE_TOTAL[(FILE_TOTAL["Time_Investment_Number"] == number)]
    on_exchange = count_company(temp)+1
    count_ = 0
    t = 0
    while count_/on_exchange < 0.5 and t <30:
        time_str = start.strftime("%Y-%m-%d")
        df = PRICE[PRICE["Time"] == time_str]
        count_ = count_company(df)
        start += datetime.timedelta(days=1)
        t +=1
    if t == 30:
        return None
    try:
        return df["Time"][df.index[0]].strftime("%Y-%m-%d")
    except:
        return None

def getDay(arr_):
    arr = []
    for number in arr_:
        arr.append(checkTime(number))
    return pd.DataFrame({"Time_Investment_Number":[number for number in arr_],
                            "Date_Buy":arr})


def getClose(symbol,start,end,Close):
    end_end = datetime.datetime(end.year,end.month,end.day+20)
    end,end_end = end.strftime("%Y-%m-%d"),end_end.strftime("%Y-%m-%d")
    df = Close[(Close['Time'] == start) & (Close['Symbol'] == symbol)].reset_index(drop=False)
    try:
        buy = df["Close"][0]
    except KeyError:
        buy = 0
    df = Close[(Close['Time'] >=end)& (Close['Time'] <= end_end) & (Close['Symbol'] == symbol)].sort_values(by=['Time']).reset_index(drop=False)
    try:
        sell = df["Close"][0]
    except KeyError:
        sell = 0
    return buy,sell

def getDividend(symbol):
    try:
        dividend = DIVIDEND[DIVIDEND["Symbol"] == symbol].reset_index()
        # dividend['Time'] = dividend['Time'].apply(lambda x: coverTime(x))
    except FileNotFoundError:
        dividend = pd.DataFrame()
    return dividend

def getSale(start,time,symbol,Close,dividend):
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
Data_Buy = getDay(pd.unique(FILE_TOTAL["Time_Investment_Number"]))
FILE_TOTAL = pd.merge(FILE_TOTAL,Data_Buy,on=["Time_Investment_Number"],how="left")

# Ghép Giá
arr_tb=[]
arr_m=[]
arr_b=[]
sym = ""
CURRENT = 0
for i in FILE_TOTAL.index:
    CURRENT+=1
    # try:
    if sym != FILE_TOTAL["Symbol"][i]:
        sym = FILE_TOTAL["Symbol"][i]
        Close = PRICE[PRICE["Symbol"] == sym].reset_index(drop=True)
        dividend = getDividend(sym)
    m,b = getSale(FILE_TOTAL["Date_Buy"][i],FILE_TOTAL["Time_Investment_Number"][i],FILE_TOTAL["Symbol"][i],Close,dividend)
    # except TypeError:
    #     print(i)
    #     m,b = 0,0
    progress_bar(CURRENT,TOTAL,text="Ghep Gia!!!")
    arr_m.append(m)
    arr_b.append(b)
FILE_TOTAL["BUY"] = arr_m
FILE_TOTAL["SELL"] = arr_b


Volume = pd.read_csv("G:/My Drive/DataVIS/VietNam/Data Lake/Distillation/All_Real/Base/Volume.csv").dropna(subset=["Date"])
Volume['Date'] = Volume["Date"].apply(lambda x: coverTime(x))
def getVolume(time,symbol):
    try:
        df = Volume[(Volume["Symbol"]==symbol)&(Volume["Date"]<=time)]
        return df["Volume"][df.index[-1]]
    except:
        return

Volume[Volume["Symbol"]=="SDH"]
FILE_TOTAL["Volume"] = FILE_TOTAL.apply(lambda row: getVolume(row["Date_Buy"],row["Symbol"]),axis=1)
Value_Volume = pd.read_csv("G:/My Drive/DataVIS/VietNam/Data Lake/Distillation/All_Real/Base/ValueTrading.csv")

def tbc(arr):
    return sum(arr)/len(arr)
def getValueTrading(day,symbol,df_value):
    df_value = df_value.sort_values(by="Time").reset_index(drop=True)
    try:
        index = df_value[df_value["Time"]==day].index[0]
        if index < 10:
            return 0,0
        else:
            volume = df_value["VolumeTrading"][index-10:index].values
            value = df_value["ValueTrading"][index-10:index].values
            return tbc(volume),tbc(value)
    except:
        return 0,0
arr_vo=[]
arr_va=[]
sym = ""
for i in FILE_TOTAL.index:
    try:
        if sym != FILE_TOTAL["Symbol"][i]:
            sym = FILE_TOTAL["Symbol"][i]
            Value = Value_Volume[Value_Volume["Symbol"] == sym].reset_index(drop=True)
        vol,val = getValueTrading(FILE_TOTAL["Date_Buy"][i],FILE_TOTAL["Symbol"][i],Value)
    except TypeError:
        vol,val = 0,0
    progress_bar(i,TOTAL,text="Ghep KLGGTB")
    # print(vol,val,FILE_TOTAL["Time"][i])
    arr_vo.append(vol)
    arr_va.append(val)

FILE_TOTAL["VolumeARG"] = arr_vo
FILE_TOTAL["ValueARG"] = arr_va
FILE_TOTAL['PROFIT'] = FILE_TOTAL['SELL']/FILE_TOTAL['BUY']
FILE_TOTAL['MARKET_CAP'] = FILE_TOTAL['BUY']*FILE_TOTAL['Volume']*1000
FILE_TOTAL.to_csv(f"{PATH_DISTILLATION_VIETNAM_ADDITIONALDATA}/{QUARTER_KEY.replace('/','_')}.csv",index=False)