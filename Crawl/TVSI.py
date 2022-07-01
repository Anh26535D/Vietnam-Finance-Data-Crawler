
import pandas as pd
from Crawl.base.URL import URL_TVSI
from .base import setup
def convertDateForLink(date):
      return date.replace("/","%2F")
      
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