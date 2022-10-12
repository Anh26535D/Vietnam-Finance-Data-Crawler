import math
import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')

from VAR_GLOBAL import *


def check_dau(a):
    if a >=0:
        return 1
    else:
        return -1

class Compare():
    def __init__(self) -> None:
        pass

    def CompareNumber(self,a,b):
        if math.isnan(a) and math.isnan(b):
            return "N"
        if math.isnan(a) or math.isnan(b):
            return "2"
        if round(a)-round(b) == 0:
            return "1"
        else:
            return "0"
    def compare_2_block(self,a,b,s_a=1,s_b=1,field=""):
        if math.isnan(a) and math.isnan(b):
            return "N"
        if math.isnan(a) or math.isnan(b):
            return "2"
        if field in ['Basic earnings per share','Diluted earnings per share']:
            s_a = 1
            s_b = 1
        dau_a = check_dau(a)
        dau_b = check_dau(b)
        a = abs(a)
        b = abs(b)
        x,y = a,b
        x = a/s_a+0.0000001
        y = b/s_b+0.0000001
        x = dau_a*x
        y = dau_b*y
        if round(x)-round(y) == 0:
            return "1"
        else:
            return "0"
    def compare_2_string(self,a,b):
        # if math.isnan(a) and math.isnan(b):
        #     return "N"
        # if math.isnan(a) or math.isnan(b):
        #     return "2"
        if a == b:
            return "1"
        else:
            return "0"

class CompareFinancial(Compare):
    def __init__(self,symbol,path_,type_time,data_field) -> None:
        self.symbol = symbol
        self.path_main = path_

        self.dict_data={
            "CF":{"path":[self.path_main+f"/Financial/CafeF/F3/{type_time}/"],"company":pd.DataFrame({}),"money":1000},
            "VS":{"path":[self.path_main+f"/Financial/VietStock/F3/{type_time}/"],"company":pd.DataFrame({}),"money":1}
        }
        self.getDataField(data_field)
        self.getData()


    def getDataField(self,data_field):
        self.data_field = data_field[["Feature"]]

    def getData(self):
        for key in self.dict_data.keys():
            try:
                df = pd.read_csv("{}/{}.csv".format(self.dict_data[key]["path"][0],self.symbol))
            except:
                df = self.field_basic
            for column in df.columns[1:]:
                df[column] = df[column].astype(float)
            df = pd.merge(self.data_field,df,on=["Feature"],how="left")
            self.dict_data[key]["company"] = df

    def getTime(self,data):
        return data.columns[1:]

    
    def get_field(self,key_1,key_2):
        df = pd.merge( self.dict_data[key_1]["company"], self.dict_data[key_2]["company"],on=["Feature"],how="inner")
        list_year = self.getTime(self.dict_data["CF"]["company"])
        s_a,s_b =  self.dict_data[key_1]["money"], self.dict_data[key_2]["money"]
        print(list_year)
        for year in list_year:
            df["Compare"] = df.apply(lambda row: self.compare_2_block(row[f"{year}_x"],row[f"{year}_y"],s_a,s_b,row["Feature"]),axis=1)
        return df