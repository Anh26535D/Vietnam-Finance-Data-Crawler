import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')
from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV
from Flow.ulis import *

class Price():
    def getClose(self,a,b):
        if math.isnan(a):
            return b/100
        return a

class TransformPrice(Price):
    def __init__(self,FU,FC,F_RANGE) -> None:
        self.FU = FU
        self.FC = FC
        self.F_RANGE = F_RANGE
        pass
    
    def ConcatData(self,LIST_PATH,symbol):
        df_close = pd.DataFrame()
        for link in LIST_PATH:
            try:
                df = pd.read_csv(f"{link}/{symbol}.csv")
            except:
                df = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
            df_close = pd.concat([df_close,df],ignore_index=True)
        return df_close.drop_duplicates(subset=["Ngày"])

    def getDataCafeF(self,symbol):
        data = self.ConcatData([self.FU.joinPath(self.FC.PATH_MAIN,date,"Close","CafeF") for date in self.F_RANGE],symbol)
        try:
            data = data[["Ngày","Giá đóng cửa"]]
        except:
            data = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
        return data[["Ngày","Giá đóng cửa"]].rename(columns={"Ngày":"Date","Giá đóng cửa":"Close"})

    def getDataStockBiz(self,symbol):
        data = self.ConcatData([self.FU.joinPath(self.FC.PATH_MAIN,date,"Close","StockBiz") for date in self.F_RANGE],symbol)
        return data[["Ngày","Đóng cửa"]].rename(columns={"Ngày":"Date","Đóng cửa":"Close"})

    def concat_source(self,symbol):
        df1 = self.getDataCafeF(symbol)
        df2 = self.getDataStockBiz(symbol)
        if df1.empty and df2.empty:
            return df1
        result = pd.merge(df1,df2,on="Date",how="outer")
        result["Date"] = result["Date"].apply(lambda x: formatDate(x))
        result["Close"] = result.apply(lambda x: self.getClose(x["Close_x"],x["Close_y"]),axis=1)
        data = result[["Date","Close"]]
        data = data.sort_values(by=['Date'],ascending=False).reset_index(drop=True)
        return data


