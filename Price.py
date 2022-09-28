import pandas as pd
from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV

PATH_ = PATH_ENV.PATH_ENV()
PATH_CAFEF = PATH_.joinPath(PATH_.PATH_CLOSE,"CafeF")
PATH_STOCKBIZ = PATH_.joinPath(PATH_.PATH_CLOSE,"StockBiz")

def getDataCafeF(symbol):
    try:
        data = pd.read_csv(f"{PATH_CAFEF}/{symbol}.csv")
    except:
        data = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
    try:
        data = data[["Ngày","Giá đóng cửa"]]
    except:
        data = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
    return data[["Ngày","Giá đóng cửa"]].rename(columns={"Ngày":"Date","Giá đóng cửa":"Close"})

def getDataStockBiz(symbol):
    try:
        data = pd.read_csv(f"{PATH_STOCKBIZ}/{symbol}.csv")
    except:
        data = pd.DataFrame({"Ngày":[],"Đóng cửa":[]})
    return data[["Ngày","Đóng cửa"]].rename(columns={"Ngày":"Date","Đóng cửa":"Close"})


def formatDate(x):
    s = x.split("/")
    return f"{s[2]}-{s[1]}-{s[0]}"

def getClose(a,b):
    if math.isnan(a):
        return b/100
    return a

def concat_source(symbol):
    df1 = getDataCafeF(symbol)
    df2 = getDataStockBiz(symbol)
    if df1.empty and df2.empty:
        return df1
    result = pd.merge(df1,df2,on="Date",how="outer")
    result["Date"] = result["Date"].apply(lambda x: formatDate(x))
    result["Close"] = result.apply(lambda x: getClose(x["Close_x"],x["Close_y"]),axis=1)
    data = result[["Date","Close"]]
    return data.sort_values(by=['Date'],ascending=False).reset_index(drop=True)

for symbol in List_Symbol:
    print(symbol)
    data = concat_source(symbol)
    data.to_csv(f"{PATH_SAVE}{symbol}.csv")