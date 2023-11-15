import datetime

PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion"

day, month, year= 0, 0, 0

if day != 0:
    date = datetime.datetime(year,month,day)
else:
    date = datetime.datetime.today()
    t = date.weekday()
    if t % 2 == 1:
        date = date - datetime.timedelta(days=1)
        
class PATH_ENV():
    '''
    Create Path for Data
    '''
    def __init__(self,Type_,date=date,RealDay=True):
        '''
        Type_: Loại data 
        date: Ngày 
        RealDay: True: Ngày thực, False: Ngày thực tế 
        CloseObject: Các đối tượng cần lấy giá 
        DividendObject: Các đối tượng cần lấy cổ tức 
        DividendPartObject: Các đối tượng cần lấy cổ tức chi tiết 
        FinancialObject: Các đối tượng cần lấy tài chính 
        FinancialPartObject: Các đối tượng cần lấy tài chính chi tiết 
        VolumeObject: Các đối tượng cần lấy khối lượng 
        VolumePartObject: Các đối tượng cần lấy khối lượng chi tiết 
        Phase: Các giai đoạn 
        Temp: Thư mục tạm 
        '''
        if RealDay == True:
            self.DateCurrent = date
            self.DayCurrent= date.strftime("%Y-%m-%d")
        else:
            self.DayCurrent = date
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
        self.Temp = "Temp"

    def joinPath(self, *args):
        """
        Join multiple paths into a directory path.
        
        Parameters
        ----------
        *args : str
            Multiple path segments to join.
        
        Returns
        -------
        str
            Joined directory path.
        """
        filtered_paths = [path for path in args if path != ""]
        joined_path = "/".join(filtered_paths)
        return joined_path

    def setFolderType(self, type):
        """
        Select the type of folder.

        Parameters
        ----------
        type : str
            Type of folder.

        Returns
        -------
        None
        """

        if type == "Ingestion":
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Ingestion"
        elif type == "Raw_VIS":
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Raw_VIS"
        elif type == "WH":
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data WareHouse"
            self.PATH_MAIN = PATH_Data
            self.PATH_CLOSE = self.joinPath(self.PATH_MAIN,"Close")
            return 
        else:
            PATH_Data = "G:\My Drive\DataVIS\VietNam\Data Lake\Data_Rule"
        self.PATH_MAIN = PATH_Data
        self.PATH_MAIN_CURRENT = self.joinPath(self.PATH_MAIN,self.DayCurrent)
        self.PATH_CLOSE = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Close")
        self.PATH_COMPARE = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Compare")
        self.PATH_FINANCIAL = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Financial")
        self.PATH_DIVIDEND = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Dividend")
        self.PATH_VOLUME = self.joinPath(self.PATH_MAIN,self.DayCurrent,"Volume")
        self.REAl_DAY = self.joinPath(self.PATH_MAIN,"RealDay")
        self.REAl_DAY_CLOSE = self.joinPath(self.REAl_DAY,'Close')
        self.REAl_DAY_IBOARD = self.joinPath(self.REAl_DAY,'RawIBoardSSI')