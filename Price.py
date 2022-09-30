import pandas as pd
from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV
def ConcatData(LIST_PATH,symbol):
    df_close = pd.DataFrame()
    for link in LIST_PATH:
        try:
            df = pd.read_csv(f"{link}/{symbol}.csv")
        except:
            df = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
        df_close = pd.concat([df_close,df],ignore_index=True)
    return df_close.drop_duplicates(subset=["Ngày"])

def getDataCafeF(symbol):
    data = ConcatData([FU.joinPath(FC.PATH_MAIN,date,"Close","CafeF") for date in F_RANGE],symbol)
    try:
        data = data[["Ngày","Giá đóng cửa"]]
    except:
        data = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
    return data[["Ngày","Giá đóng cửa"]].rename(columns={"Ngày":"Date","Giá đóng cửa":"Close"})

def getDataStockBiz(symbol):
    data = ConcatData([FU.joinPath(FC.PATH_MAIN,date,"Close","StockBiz") for date in F_RANGE],symbol)
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
    data = data.sort_values(by=['Date'],ascending=False).reset_index(drop=True)
    data.to_csv(f"{FU.PATH_CLOSE}/{symbol}.csv",index=False)

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    try:
        concat_source(symbol)
    except:
        pass
