import pandas as pd
from Crawl.base.URL import URL_STOCK_BIZ
from .base import setup

class Close(setup.Setup):    
    def __init__(self,symbol="AAA",end='09/06/2022'):
        super().__init__()
        self.URL_CLOSE = URL_STOCK_BIZ["CLOSE"].replace("SYMBOL",symbol)
        self.symbol=symbol
        self.date = end
        
    def fix_url(self):
        return self.URL_CLOSE+self.date

    def DownloadClose(self):
        return self.download_one_close().drop_duplicates(subset=['Ngày'])

    def download_one_close(self):
        stock_data = pd.DataFrame({})
        for i in range(1000):
            stock_slice_batch = self.download_batch_get_request(self.fix_url(),{"class":"dataTable"})
            stock_data = pd.concat([stock_data, stock_slice_batch], axis=0)
            try:
              self.date = stock_slice_batch["Ngày"].values[-1]
              date_end_batch = stock_slice_batch["Ngày"].values[2]
            except:
                break
        return stock_data