from Crawl import CafeF
from Crawl import StockBiz
import pandas as pd
from Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV()
start = PATH_.DateCurrent - datetime.timedelta(days=365)
start = start.strftime("%d/%m/%Y")
end = PATH_.DateCurrent.strftime("%d/%m/%Y")


def closeCafeF(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_CLOSE,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        com = CafeF.Close(symbol=symbol,start=start,end=end)
        com.DownloadClose().to_csv(f"{PATH}/{symbol}.csv")
    
def closeStockBiz(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_CLOSE,"StockBiz")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        com = StockBiz.Close(symbol=symbol,start=end,end=start)
        com.DownloadClose().to_csv(f"{PATH}/{symbol}.csv")

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    print(symbol)
    closeCafeF(symbol)
    closeStockBiz(symbol)
# closeCafeF("AAA")
# closeStockBiz("AAA")
