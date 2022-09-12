from datetime import datetime

PATH_Data = "C:\DataVietNam\Data"

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
    
    def joinPath(self,*arg):
        return "/".join(arg)
    

