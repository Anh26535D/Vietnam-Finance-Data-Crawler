import json
import time
import pandas as pd
import shutil
import sys
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')


from base.Setup import *


def read_file(path,file_type):
    if file_type == ".csv":
        try:
            pd.read_csv(path)
            return True
        except:
            return False
    elif file_type == ".json":
        try:
            f = open(path, encoding="utf8")
            json.load(f)
            return True
        except:
            return False
    return False    


def File(list_symbol,F_RANGE,source,type_time,field,file_type=".csv",type_data = "Financial"):
    for symbol in list_symbol:
        for index in range(len(F_RANGE)-1,-1,-1):
            date = F_RANGE[index]
            path = FC.joinPath(FC.PATH_MAIN,date,type_data,source,type_time,field,f"{symbol}{file_type}")
            if read_file(path,file_type) == True:
                print(path)
                path_from = path
                path_to = FC.joinPath(FU.PATH_MAIN,F_END,type_data,source,"F0",type_time,field)
                shutil.copy2(path_from, path_to)
                break

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Year","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Year","IncomeStatement")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Quarter","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Quarter","IncomeStatement")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Year","BalanceSheet",".json")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Year","IncomeStatement",".json")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Quarter","BalanceSheet",".json")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Quarter","IncomeStatement",".json")
File(List_Symbol["Mã CK▲"],F_RANGE,source="CafeF",type_time="",field="VolumeNow",type_data="Volume")
File(List_Symbol["Mã CK▲"],F_RANGE,source="VietStock",type_time="",field="VolumeNow",type_data="Volume")
File(List_Symbol["Mã CK▲"],F_RANGE,source="CafeF",type_time="",field="",type_data="Close")
File(List_Symbol["Mã CK▲"],F_RANGE,source="StockBiz",type_time="",field="",type_data="Close")
File(List_Symbol["Mã CK▲"],F_RANGE,source="CafeF",type_time="",field="",type_data="Dividend")
File(List_Symbol["Mã CK▲"],F_RANGE,source="VietStock",type_time="",field="CashDividend",type_data="Dividend")
File(List_Symbol["Mã CK▲"],F_RANGE,source="VietStock",type_time="",field="BonusShare",type_data="Dividend")
File(List_Symbol["Mã CK▲"],F_RANGE,source="VietStock",type_time="",field="StockDividend",type_data="Dividend")
