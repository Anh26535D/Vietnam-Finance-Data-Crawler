
from Crawl import TVSI
from Crawl import StockBiz
# import multiprocessing
import pandas as pd
# path = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/TVSI/Financial/Quarter/BalanceSheet/'
# PATH = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/TVSI/Financial/Quarter/IncomeStatement/'
PATH = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/StockBiz/Close/'
def close(symbol):
    try:
        df = pd.read_csv(PATH+symbol+".csv")
    except:
        com = StockBiz.Close(symbol=symbol)
        com.DownloadClose().to_csv(f"{PATH}{symbol}.csv")
# def finan(symbol):
#     try:
#         df = pd.read_csv(PATH+symbol+".csv")
#     except:
#         print(symbol,end=" ")
#         com = TVSI.Financail(symbol=symbol)
#         com.get_Balance_Year(2000,2022).to_csv(PATH+symbol+".csv",index=False)
#         print(symbol,"Done!!!")
# finan("AAA")

data = pd.read_csv("/content/List_Com_DateUpDownExchange.xlsx - Sheet1.csv")
Symbol = data["Symbol"]
for i in Symbol[1000:]:
    try:
        print(i,end="")
        close(i)
    except:
        print("---loi")
    print()
# def multip():
#     pool = multiprocessing.Pool(processes=4)
#     for symbol in Symbol:
#         pool.apply_async(close,args=(symbol,))
#     pool.close()
#     pool.join()

# if __name__ == '__main__':
#     multip()

