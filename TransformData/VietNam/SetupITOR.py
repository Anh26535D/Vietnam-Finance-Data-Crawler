import json
import pandas as pd
import shutil
import sys
sys.path.append(r'C:\DataVietNam')
from Flow import Folder

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

def read_file(path,file_type):
    if file_type == ".csv":
        try:
            pd.read_csv(path)
            return True
        except:
            return False
    elif file_type == ".json":
        try:
            f = open (path, "r")
            json.loads(f.read())
            return True
        except:
            return False
    return False    


def File(list_symbol,F_RANGE,source,type_time,field):
    file_type = ".csv"
    if source == "CafeF":
        file_type = ".json"
    for symbol in list_symbol:
        for index in range(len(F_RANGE)-1,-1,-1):
            date = F_RANGE[index]
            path = FC.joinPath(FC.PATH_MAIN,date,"Financial",source,type_time,field,f"{symbol}{file_type}")
            print(path)
            if read_file(path,file_type) == True:
                path_from = path
                path_to = FC.joinPath(FU.PATH_MAIN,F_END,"Financial",source,"F0",type_time,field)
                shutil.copy2(path_from, path_to)
                break
            
List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Year","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Year","IncomeStatement")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Quarter","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"VietStock","Quarter","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Year","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Year","IncomeStatement")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Quarter","BalanceSheet")
File(List_Symbol["Mã CK▲"],F_RANGE,"CafeF","Quarter","IncomeStatement")