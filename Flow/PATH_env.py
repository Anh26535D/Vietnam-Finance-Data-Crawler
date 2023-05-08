import datetime

# PATH_Data = "C:\Data"
PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion"

# day,month,year=0,0,0
# day,month,year=31,3,2023
day,month,year=5,4,2023
if day != 0:
    date = datetime.datetime(year,month,day)
else:
    date = datetime.datetime.today()
    t = date.timetuple().tm_wday
    # if t % 2 != 0:
    #     date = date - datetime.timedelta(days=1)
        
class PATH_ENV():
    def __init__(self,Type_,date=date):
        self.DateCurrent = date
        self.DayCurrent= date.strftime("%Y-%m-%d")
        self.setTypeForder(Type_)
        self.CloseObject = ["CafeF","StockBiz"]
        self.DividendObject = ["CafeF","VietStock"]
        self.DividendPartObject = ["CashDividend","BonusShare","StockDividend"]
        self.FinancialObject = ["CafeF","VietStock"]
        self.Type_Time = ["Year","Quarter"]
        self.FinancialPartObject = ["BalanceSheet","IncomeStatement","CashFlowDirect","CashFlowInDirect"]
        self.VolumeObject = ["CafeF","VietStock","TVSI"]
        self.VolumePartObject = ["TreasuryShares","VolumeAdditionailEvents","VolumeNow"]
        self.Phase = [f"F{i}" for i in range(4)]

    def joinPath(self,*arg):
        arr = []
        for i in arg:
            if i != "":
                arr.append(i)
        return "/".join(arr)

    def setTypeForder(self,Type):
        if Type == "Ingestion":
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion"
        elif Type == "Raw_VIS":
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS"
        else:
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Data_Rule"
        self.PATH_MAIN = PATH_Data
        self.PATH_MAIN_CURRENT = self.joinPath(self.PATH_MAIN,self.DayCurrent)
        self.PATH_CLOSE = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Close")
        self.PATH_COMPARE = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Compare")
        self.PATH_FINANCIAL = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Financial")
        self.PATH_DIVIDEND = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Dividend")
        self.PATH_VOLUME = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Volume")
            
    

