from datetime import datetime

# PATH_Data = "C:\Data"
PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion"

day,month,year=0,0,0
if day != 0:
    date = datetime.datetime(year,month,day)
else:
    date = datetime.today()


class PATH_ENV():
    def __init__(self):
        self.PATH_MAIN = PATH_Data
        self.DateCurrent = date
        self.DayCurrent= date.strftime("%Y-%m-%d")
        self.PATH_MAIN_CURRENT = self.joinPath(self.PATH_MAIN,self.DayCurrent)
        self.PATH_CLOSE = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Close")
        self.PATH_FINANCIAL = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Financial")
        self.PATH_DIVIDEND = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Dividend")
        self.PATH_VOLUME = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Volume")
        self.CloseObject = ["CafeF","StockBiz"]
        self.DividendObject = ["CafeF","VietStock"]
        self.DividendPartObject = ["CashDividend","BonusShare","StockDividend"]
        self.FinancialObject = ["CafeF","VietStock"]
        self.Type_Time = ["Year","Quarter"]
        self.FinancialPartObject = ["BalanceSheet","IncomeStatement","CashFlowDirect","CashFlowInDirect"]
        self.VolumeObject = ["CafeF","VietStock"]
        self.VolumePartObject = ["TreasuryShares","VolumeAdditionailEvents","VolumeNow"]

    def joinPath(self,*arg):
        return "/".join(arg)
    

