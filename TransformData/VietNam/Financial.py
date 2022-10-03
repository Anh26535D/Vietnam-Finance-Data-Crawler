import json
import math
import pandas as pd
import re
import os
import numpy as np
class TransForm():
    def __init__(self,dict_path_) -> None:
        self.path_object = dict_path_
        pass

class CafeF(TransForm):
    def __init__(self,dict_path_cf) -> None:
        super().__init__(dict_path_cf)
        self.data_field={}
        df = pd.read_excel("/content/BalanceSheet.xlsx",sheet_name="CafeF")
        df = df.rename(columns={"Cafef_Raw":"field"})
        self.data_field["Balance"]=df

        df = pd.read_excel("/content/IncomeStatement.xlsx",sheet_name="CafeF")
        df = df.rename(columns={"Cafef_Raw":"field"})
        self.data_field["Income"]=df

    def Financial_F0_to_F1(self,symbol,field):
        list_ = []
        try:
            with open(f'{self.path_object["F0"][field]}/{symbol}.json', "r",encoding='utf8') as j:
                    data = json.loads(j.read())
            temp = pd.DataFrame({"field": []})
            for key in list(data.keys()):
                try:
                    df = pd.DataFrame.from_records(data[key])
                    dict_ = {}
                    for i in df.index:
                        df["field"][i] = ''.join([i for i in df["field"][i] if not i.isdigit()])
                        dict_[df["field"][i]] = 0
                
                    for i in df.index:
                        dict_[df["field"][i]]+=1
                        df["field"][i] = df["field"][i]+"__"+str(dict_[df["field"][i]])
                        col_key = []

                    for i in df:
                        if i in temp.columns:
                            col_key.append(i)
                    temp = pd.merge(temp, df, on=col_key, how="outer")
                except:
                    pass
            arr = []
            for col in temp.columns:
                try:
                    match = re.findall('([0-9]-[0-9]+)', col)
                    time = match[0].replace("-","/")
                    arr.append(time)
                except:
                    arr.append(col)
            temp.columns = arr
            temp.to_csv(self.path_object["F1"][field]+symbol+".csv",index=False)
            return temp
        except:
            print(symbol,field)
            return -1

    def Financial_F1_to_F2(self,symbol,field):
            try:
                link ="{}{}.csv".format(self.path_object["F1"][field],symbol)
                data = pd.read_csv(link)
                temp = pd.merge(self.data_field[field.split("_")[0]],data, on="field",how="outer")
                temp = temp.drop(columns=["field"])
                for column in temp.columns[1:]:
                    temp[column] = temp[column].astype(float)
                temp = temp.groupby("Feature").max().reset_index()
                temp.to_csv(self.path_object["F2"][field]+symbol+".csv",index=False)
                return temp
            except:
                print(symbol)
                return -1

    def run(self,func,symbol):
        func(symbol,"Balance_Quater")
        func(symbol,"Income_Quater")
        func(symbol,"Balance_Year")
        func(symbol,"Income_Year")

class VietStock(TransForm):
    def __init__(self,dict_path_vs) -> None:
        super().__init__(dict_path_vs)
        pass
    
    def change_data_BS(self,df_finan):
        first_col = df_finan.columns[0]
        feature_change  = '- Nguyên giá__' + df_finan[first_col].loc[df_finan[df_finan[first_col]=='- Nguyên giá'].index-1]
        feature_change.index = feature_change.index+1
        df_finan[first_col].iloc[df_finan[df_finan[first_col]=='- Nguyên giá'].index] = feature_change

        feature_change  = '- Giá trị hao mòn lũy kế (*)__' + df_finan[first_col].loc[df_finan[df_finan[first_col]=='- Giá trị hao mòn lũy kế (*)'].index-2]
        feature_change.index = feature_change.index+2
        df_finan[first_col].iloc[df_finan[df_finan[first_col]=='- Giá trị hao mòn lũy kế (*)'].index] = feature_change
        return df_finan
    def Financail_F0_to_F1(self,symbol,field):
        path_in = self.path_object["F0"][field]
        path_out = self.path_object["F1"][field]
        if os.path.exists(f'{path_in}{symbol}.csv'):
            df = pd.read_csv(f'{path_in}{symbol}.csv')
            df = self.change_data_BS(df)
            df.to_csv(f'{path_out}{symbol}.csv', index = False)
    
    def Financail_F1_to_F2(self,symbol,field):
        df = pd.read_csv(f'{self.path_object["F1"][field]}/{symbol}.csv')
        if len(df.index) == 0:
            return df
        df =df[6:].reset_index(drop = True)
        first_col = df.columns[0]
        df = df.rename(columns = {first_col:'VIS_Raw'})
        df_concat = pd.merge(df, df, how = 'right', on = ['VIS_Raw'])
        if all(df_concat['VIS_Raw'] == df_concat['VIS_Raw']) == True:
            df = pd.concat([df, df], axis = 1).drop(columns = ['VIS_Raw', 'Unnamed: 1', 'Unnamed: 2', 'Field_Raw'])
            return df
        else: 
            return False

def check_dau(a):
    if a >=0:
        return 1
    else:
        return -1
        
class Compare():
    def __init__(self,symbol,path_) -> None:
        self.symbol = symbol
        self.path_main = path_

        self.dict_data={
            "CF":{"path":[self.path_main+"CafeF/Financial/Financial_F3/Quarter/BalanceSheet/",self.path_main+"CafeF/Financial/Financial_F3/Quarter/IncomeStatement/"],"company":pd.DataFrame({}),"money":1000},
            "VS":{"path":[self.path_main+"Vietstock/Financial/Financial_F3/Quarter/BalanceSheet/",self.path_main+"Vietstock/Financial/Financial_F3/Quarter/IncomeStatement/"],"company":pd.DataFrame({}),"money":1}
        }
        self.getDataField()
        self.getData()

    def getDataField(self):
        data_field = pd.read_excel("/content/Feature_Standard_Library.xlsx",sheet_name="Quarter")
        data_field = data_field.rename(columns={"column":"Feature"})
        self.data_field = data_field[["Feature"]]

    def getData(self):
        for key in self.dict_data.keys():
            try:
                df_b = pd.read_csv("{}/{}.csv".format(self.dict_data[key]["path"][0],self.symbol))
                df_i = pd.read_csv("{}/{}.csv".format(self.dict_data[key]["path"][1],self.symbol))
                df = pd.concat([df_b,df_i],ignore_index=True)
            except:
                df = self.field_basic
            for column in df.columns[1:]:
                df[column] = df[column].astype(float)
            df = pd.merge(self.data_field,df,on=["Feature"],how="left")
            df.replace(0, np.nan, inplace=True)
            df = df.dropna(axis=1, how='all')
            df = df.fillna(0)
            for column in  self.dict_data["other"]["list_year"]:
                if not(column in df.columns):
                    df[column]=[np.nan for i in df["Feature"]]
            df = df[ self.dict_data['other']["list_year"]]
            self.dict_data[key]["company"] = df

    def compare_2_block(self,a,b,s_a,s_b,field):
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
    
    def get_field(self,key_1,key_2):
        df = pd.merge( self.dict_data[key_1]["company"], self.dict_data[key_2]["company"],on=["Feature"],how="inner")
        list_year =  self.dict_data["other"]["list_year"]
        s_a,s_b =  self.dict_data[key_1]["money"], self.dict_data[key_2]["money"]
        for year in list_year[1:]:
            df[year] = df.apply(lambda row: self.compare_2_block(row[f"{year}_x"],row[f"{year}_y"],s_a,s_b,row["Feature"]),axis=1)
            df = df.drop(columns=[f"{year}_x",f"{year}_y"])
        return df
