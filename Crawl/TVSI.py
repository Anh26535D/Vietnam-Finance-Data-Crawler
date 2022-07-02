
import math
import pandas as pd
from Crawl.base.URL import URL_TVSI
from .base import setup
def convertDateForLink(date):
      return date.replace("/","%2F")
class Financail(setup.Setup):
    def __init__(self,symbol="AAA",start="10/06/2021",end="10/10/2021"):
        super().__init__()
        self.symbol = symbol
        self.URL_BALANCED = URL_TVSI["BALANCE_SHEET_QUARTER"]
        self.URL_INCOME = URL_TVSI["INCOME_STATEMENT_QUARTER"]
    
    def getFinanStatement(self,link):
        table = self.download_batch_get_request(link)
        table = table.rename(columns=table.iloc[0])
        table = table.drop(table.index[0])
        table = table.dropna(axis=1, how='all')
        arr = []
        for i in table.columns:
            if str(i) == "nan":
                arr.append("field")
            else:
                arr.append(i)
        table.columns = arr
        return table
    
    def get_Table(self,year,table):
        arr = ['field']
        for col in table.columns:
            if col.find(str(year))!=-1:
                arr.append(col)
        return table[arr]
    
    def get_Data_Table(self,link,year):
        table = self.getFinanStatement(link.replace("SYMBOL",self.symbol).replace("YEAR",str(year)))
        return self.get_Table(year,table)
    
    def get_Data_Link(self,start,end,link):
        if self.checkstatus_TVSI(link.replace("SYMBOL",self.symbol).replace("YEAR",str(start))):
            result = pd.DataFrame({"field":[]})
            list_field = []
            for i in range(start,end+1):
                try:
                    df1 = self.get_Data_Table(link,i)
                    for col in df1.columns:
                        if col in result.columns:
                            list_field.append(col)
                    result = pd.merge(df1,result,on=list_field,how='outer')
                except:
                    pass
        else:
            return
        return result

    def get_Balance(self,start,end):
        return self.get_Data_Link(start,end,self.URL_BALANCED)
    def get_Income(self,start,end):
        return self.get_Data_Link(start,end,self.URL_INCOME)

class Close(setup.Setup):
    def __init__(self,symbol="AAA",start="10/06/2021",end="10/10/2021"):
        super().__init__()
        self.URL_CLOSE = URL_TVSI["CLOSE"]
        self.symbol=symbol
        self.start = start
        self.end = end
    def DownloadClose(self):
        return self.download_one_close()
    def fix_link(self,page):
        return self.URL_CLOSE.replace("SYMBOL",self.symbol).replace("PAGE",str(page)).replace("DATE_START",convertDateForLink(self.start)).replace("DATE_END",convertDateForLink(self.end))
    def download_one_close(self):
        stock_data = pd.DataFrame({})
        for i in range(1000):
            url = self.fix_link(i + 1)
            stock_slice_batch = self.download_batch_get_request(url)
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
                date_end_batch = stock_slice_batch["Ngày"].values[-1]
            except:
                break
        return stock_data