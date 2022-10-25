import sys
sys.path.append(r'C:\DataVietNam')
from Flow import Folder
from VAR_GLOBAL import *

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

# F_START = FU.GetDateUpdateEndStart()
F_START = FU.GetDateUpdateEndStart(day=START_DAY_UPDATE)
F_END = FU.GetDateUpdateEnd(day=END_DAY_UPDATE)
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>=F_START and date <= F_END:
        F_RANGE.append(date)

class TieuChuan():
    def __init__(self) -> None:
        self.Financial = {
            "VS":{
                "BalanceSheet": {"Min_row":120,"Max_row":135,"Columns":5},
                "IncomeStatement": {"Min_row":25,"Max_row":35,"Columns":5}
            }
        }
    
    def CheckDataFinancial(self,key,data,source="VS"):
        if not key in self.Financial[source].keys():
            return True
            
        cols = data.columns
        rows = len(data.index)
        if len(cols) != self.Financial[source][key]["Columns"]:
            return False
        if self.Financial[source][key]["Min_row"] > rows:
            return False
        if  self.Financial[source][key]["Max_row"] < rows:
            return False
        return True
    
        

print(F_START,F_END,F_RANGE)