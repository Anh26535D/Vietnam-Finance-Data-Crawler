import sys
import pandas as pd
sys.path.append(r'C:\DataVietNam')
from Flow import Folder
from VAR_GLOBAL_CONFIG import *

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

# F_START = FU.GetDateUpdateEndStart()
# F_START = FU.GetDateUpdate(START_DAY_UPDATE)
# F_END = FU.GetDateUpdate(END_DAY_UPDATE)
F_START = START_DAY_UPDATE
F_END = END_DAY_UPDATE
F_BASE = FC.getListPath()
F_RANGE = []

for date in F_BASE:
    if date>=F_START and date <= F_END:
        F_RANGE.append(date)

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
# SYMBOL = List_Symbol[List_Symbol["Sàn"]=="HOSE"]["Mã CK▲"]
SYMBOL = List_Symbol["Mã CK▲"]
# SYMBOL = ["ASP","DAH","VNE"]
TOTAL = len(SYMBOL)
print(TOTAL,SYMBOL)

# List_Symbol = pd.read_excel(f'G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS/2022-11-01\Compare/1_Financial_Quarter.xlsx',sheet_name="Trang tính1")
# SYMBOL = List_Symbol["Symbol_Thieu"]
# TOTAL = len(SYMBOL)

class TieuChuan():
    def __init__(self) -> None:
        self.Financial = {
            "VietStock":{
                "BalanceSheet": {"Min_row":115,"Max_row":135,"Columns":5},
                "IncomeStatement": {"Min_row":20,"Max_row":35,"Columns":5}
            },
            "CafeF":{
                "BalanceSheet": {"Min_row":115,"Max_row":135},
                "IncomeStatement": {"Min_row":20,"Max_row":30}
            }
        }
    
    def CheckDataFinancial(self,key,data,source="VietStock"):
        if not key in self.Financial[source].keys():
            return True
        if source == "VietStock":    
            cols = data.columns
            rows = len(data.index)
            if len(cols) != self.Financial[source][key]["Columns"]:
                return False
            if self.Financial[source][key]["Min_row"] > rows:
                return False
            if  self.Financial[source][key]["Max_row"] < rows:
                return False
            return True
        elif source == "CafeF":
            keys = list(data.keys())
            rows = len(data[keys[0]])
            # print(rows,self.Financial[source][key]["Min_row"])
            if self.Financial[source][key]["Min_row"] > rows:
                return False
            if  self.Financial[source][key]["Max_row"] < rows:
                return False
            return True
        return False
        
print(F_START,F_END,F_RANGE)