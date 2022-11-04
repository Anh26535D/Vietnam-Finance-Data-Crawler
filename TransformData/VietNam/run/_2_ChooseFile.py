import json
import time
import pandas as pd
import shutil
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from Flow.ulis import *
from base.Setup import *

T = TieuChuan()

def read_file(path,file_type,field):
    if file_type == ".csv":
        try:
            data = pd.read_csv(path)
            return T.CheckDataFinancial(field,data)
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
    CURRENT = 0
    for symbol in list_symbol:
        CURRENT+=1
        progress_bar(CURRENT,TOTAL,text=f"Lấy Giá {source},{field}")
        for index in range(len(F_RANGE)-1,-1,-1):
            date = F_RANGE[index]
            path = FC.joinPath(FC.PATH_MAIN,date,type_data,source,type_time,field,f"{symbol}{file_type}")
            if read_file(path,file_type,field) == True:
                path_from = path
                path_to = FC.joinPath(FU.PATH_MAIN,F_END,type_data,source,"F0",type_time,field)
                shutil.copy2(path_from, path_to)
                break
# File(SYMBOL,F_RANGE,"VietStock","Year","BalanceSheet")
# File(SYMBOL,F_RANGE,"VietStock","Year","IncomeStatement")
File(SYMBOL,F_RANGE,"VietStock","Quarter","BalanceSheet")
File(SYMBOL,F_RANGE,"VietStock","Quarter","IncomeStatement")
# File(SYMBOL,F_RANGE,"CafeF","Year","BalanceSheet",".json")
# File(SYMBOL,F_RANGE,"CafeF","Year","IncomeStatement",".json")
# File(SYMBOL,F_RANGE,"CafeF","Quarter","BalanceSheet",".json")
# File(SYMBOL,F_RANGE,"CafeF","Quarter","IncomeStatement",".json")
# File(SYMBOL,F_RANGE,source="CafeF",type_time="",field="VolumeNow",type_data="Volume")
# File(SYMBOL,F_RANGE,source="VietStock",type_time="",field="VolumeNow",type_data="Volume")
# File(SYMBOL,F_RANGE,source="CafeF",type_time="",field="",type_data="Dividend")
# File(SYMBOL,F_RANGE,source="VietStock",type_time="",field="CashDividend",type_data="Dividend")
# File(SYMBOL,F_RANGE,source="VietStock",type_time="",field="BonusShare",type_data="Dividend")
# File(SYMBOL,F_RANGE,source="VietStock",type_time="",field="StockDividend",type_data="Dividend")
