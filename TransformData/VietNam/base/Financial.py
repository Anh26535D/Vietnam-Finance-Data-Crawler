import datetime
import json
import math
import pandas as pd
import re
import os
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import sys
sys.path.append(r'C:\DataVietNam')
from VAR_GLOBAL import *

class TransForm():
    def __init__(self,dict_path_) -> None:
        self.path_object = dict_path_
        self.time = []
        pass
    def replace_NaN_0(self,df):
        df = df.dropna(axis=1, how='all')
        df = df.fillna(0)
        for column in self.time:
            if not(column in df.columns):
                df[column]=[np.nan for i in df["Feature"]]
        return df
        
    def getTime(self,type_time):
        if type_time == "Year":
            return YEAR_KEY
        elif type_time == "Quarter":
            return QUARTER_KEY

class CafeF(TransForm):
    def __init__(self,dict_path_cf) -> None:
        super().__init__(dict_path_cf)
        df = pd.read_excel(f'{dict_path_cf["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="CafeF")
        df = df.rename(columns={"VIS_Raw_F1":"field"})
        self.data_field = df
        df = pd.read_excel(f'{dict_path_cf["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="Total")
        self.data_field_default_year = df
        df = pd.read_excel(f'{dict_path_cf["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="Quarter")
        self.data_field_default_quarter = df

    def Financial_F0_to_F1(self,symbol,type_time):
            data = {}
            for key in self.path_object["F0"].keys():
                if key.find(type_time) != -1:
                    with open(f'{self.path_object["F0"][key]}/{symbol}.json',encoding='utf8') as j:
                            data1 = json.loads(j.read())
                    for key,value in data1.items():
                        try:
                            data[key] = data[key]+data1[key]
                        except:
                            data[key] = []
                            data[key] = data[key]+data1[key]

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
                    time = time.split("-")
                    time = "-".join([time[i] for i in range(len(time)-1,-1,-1)])
                    arr.append(time)
                except:
                    arr.append(col)
            temp.columns = arr
            temp.to_csv(f'{self.path_object["F1"][type_time]}/{symbol}.csv',index=False)
            return temp

    def Financial_F1_to_F2(self,symbol,type_time):
                link ="{}/{}.csv".format(self.path_object["F1"][type_time],symbol)
                data = pd.read_csv(link)
                temp = pd.merge(self.data_field,data, on="field",how="outer")
                temp = temp.drop(columns=["field"])
                for column in temp.columns[1:]:
                    temp[column] = temp[column].astype(float)
                temp = temp.groupby("Feature").max().reset_index()
                temp.columns = [col.replace("]","").replace("[","") for col in temp.columns]
                temp.to_csv(f'{self.path_object["F2"][type_time]}/{symbol}.csv',index=False)
                return temp
    def Financial_F2_to_F3(self,symbol,type_time):
                if type_time == "Year":
                    data_field = self.data_field_default_year
                elif type_time == "Quarter":
                    data_field = self.data_field_default_quarter
                link ="{}/{}.csv".format(self.path_object["F2"][type_time],symbol)
                data = pd.read_csv(link)
                self.time=data.columns[1:]

                data = self.replace_NaN_0(data)

                temp = pd.merge(data_field,data, on="Feature",how="inner")
                temp = temp[[data.columns[0],self.getTime(type_time)]]
                temp.to_csv(f'{self.path_object["F3"][type_time]}/{symbol}.csv',index=False)
                return temp
    
    def run(self,symbol,type_time):
        try:
            self.Financial_F0_to_F1(symbol,type_time)
            self.Financial_F1_to_F2(symbol,type_time)
            self.Financial_F2_to_F3(symbol,type_time)
        except:
            print(symbol,type_time)
            return False
        return True


class VietStock(TransForm):
    def __init__(self,dict_path_vs) -> None:
        super().__init__(dict_path_vs)
        df = pd.read_excel(f'{dict_path_vs["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="VietStock")
        df = df.rename(columns={"VIS_Raw_F1":"field"})
        self.data_field = df
        df = pd.read_excel(f'{dict_path_vs["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="Total")
        self.data_field_default_year = df
        df = pd.read_excel(f'{dict_path_vs["Feature"]}/Feature_Standard_Library.xlsx',sheet_name="Quarter")
        self.data_field_default_quarter = df
    
    def change_data_BS(self,df_finan):
        first_col = df_finan.columns[0]
        feature_change  = '- Nguyên giá__' + df_finan[first_col].loc[df_finan[df_finan[first_col]=='- Nguyên giá'].index-1]
        feature_change.index = feature_change.index+1
        df_finan[first_col].iloc[df_finan[df_finan[first_col]=='- Nguyên giá'].index] = feature_change

        feature_change  = '- Giá trị hao mòn lũy kế (*)__' + df_finan[first_col].loc[df_finan[df_finan[first_col]=='- Giá trị hao mòn lũy kế (*)'].index-2]
        feature_change.index = feature_change.index+2
        df_finan[first_col].iloc[df_finan[df_finan[first_col]=='- Giá trị hao mòn lũy kế (*)'].index] = feature_change
        return df_finan
    def Financial_F0_to_F1(self,symbol,type_time):
        data = pd.DataFrame({})
        for key in self.path_object["F0"].keys():
            if key.find(type_time) != -1:
                path_in = self.path_object["F0"][key]
                if os.path.exists(f'{path_in}/{symbol}.csv'):
                    df = pd.read_csv(f'{path_in}/{symbol}.csv')
                    df = self.change_data_BS(df)
                    data = pd.concat([data,df],ignore_index=True)
        path_out = self.path_object["F1"][type_time]
        data.to_csv(f'{path_out}/{symbol}.csv', index = False)

    def Financial_F1_to_F2(self,symbol,type_time):
        df = pd.read_csv(f'{self.path_object["F1"][type_time]}/{symbol}.csv')
        if len(df.index) == 0:
            return df
        df =df[6:].reset_index(drop = True)
        first_col = df.columns[0]
        df = df.rename(columns = {first_col:'field'})
        df_concat = pd.merge(self.data_field, df, how = 'left', on = ['field'])
        if all(df_concat['field'] == df_concat['field']) == True:
            df = df_concat.drop(columns = ["Ingestion", 'Unnamed: 1', 'Unnamed: 2',"field"])
            df = df.rename(columns={"VIS_Raw_F2":"Feature"})
            df.columns = [col.replace("Q","") for col in df.columns]
            path_out = self.path_object["F2"][type_time]
            df.to_csv(f'{path_out}/{symbol}.csv', index = False)
            return df
        else: 
            return False

    def Financial_F2_to_F3(self,symbol,type_time):
            if type_time == "Year":
                data_field = self.data_field_default_year
            elif type_time == "Quarter":
                data_field = self.data_field_default_quarter

            link ="{}/{}.csv".format(self.path_object["F2"][type_time],symbol)
            data = pd.read_csv(link)

            self.time=data.columns[1:]

            data = self.replace_NaN_0(data)
            temp = pd.merge(data_field,data, on="Feature",how="inner")
            temp = temp[[data.columns[0],self.getTime(type_time)]]
            temp.to_csv(f'{self.path_object["F3"][type_time]}/{symbol}.csv',index=False)
            return temp
    def run(self,symbol,type_time):
        try:
            self.Financial_F0_to_F1(symbol,type_time)
            self.Financial_F1_to_F2(symbol,type_time)
            self.Financial_F2_to_F3(symbol,type_time)
        except:
            print(symbol,type_time)
            return False
        return True

