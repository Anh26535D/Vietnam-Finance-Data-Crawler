import pandas as pd
import re
import json
from Flow import Folder
from PATH_FINANCAIL import *
FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

def ConcatData(LIST_PATH,symbol):
    df_close = pd.DataFrame()
    for link in LIST_PATH:
        try:
            with open(f'{dict_path[F_FROM][field]}{symbol}.json', "r",encoding='utf8') as j:
                data = json.loads(j.read())
        except:
            df = pd.DataFrame({"Ngày":[],"Giá đóng cửa":[]})
        df_close = pd.concat([df_close,df],ignore_index=True)
    return df_close.drop_duplicates(subset=["Ngày"])



def Financial(symbol,field):
        list_ = []
        try:
            with open(f'{dict_path[F_FROM][field]}{symbol}.json', "r",encoding='utf8') as j:
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
            temp.to_csv(dict_path[F_TO][field]+symbol+".csv",index=False)
            return temp
        except:
            print(symbol,field)
            return -1
F_FROM = "F0"
F_TO = "F1"
for symbol in list_symbol:
    Financial(symbol,"Balance_Quater")
    Financial(symbol,"Income_Quater")
    Financial(symbol,"InDirect_Quater")
    Financial(symbol,"Direct_Quater")

data_field={}
df = pd.read_excel("/content/BalanceSheet.xlsx",sheet_name="CafeF")
df = df.rename(columns={"Cafef_Raw":"field"})
data_field["Balance"]=df

df = pd.read_excel("/content/IncomeStatement.xlsx",sheet_name="CafeF")
df = df.rename(columns={"Cafef_Raw":"field"})
data_field["Income"]=df

df = pd.read_excel("/content/CashFlowInDirect.xlsx",sheet_name="Cafef")
df = df.rename(columns={"Cafef_Raw_InDirect":"field"})
data_field["InDirect"]=df

df = pd.read_excel("/content/CashFlowDirect.xlsx",sheet_name="Cafef")
df = df.rename(columns={"Cafef_Raw_Direct":"field"})
data_field["Direct"]=df
def FinancialF2(symbol,field):
        try:
            link ="{}{}.csv".format(dict_path[F_FROM][field],symbol)
            data = pd.read_csv(link)
            print(link)
            temp = pd.merge(data_field[field.split("_")[0]],data, on="field",how="outer")
            temp = temp.drop(columns=["field"])
            for column in temp.columns[1:]:
                temp[column] = temp[column].astype(float)
            temp = temp.groupby("Feature").max().reset_index()
            temp.to_csv(dict_path[F_TO][field]+symbol+".csv",index=False)
            return temp
        except:
            print(symbol)
            return -1

F_FROM = "F1"
F_TO = "F2"


List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    try:
        FinancialF2(symbol,"Balance_Quater")
        FinancialF2(symbol,"Income_Quater")
        FinancialF2(symbol,"Direct_Quater")
        FinancialF2(symbol,"InDirect_Quater")
    except:
        pass