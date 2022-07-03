from Crawl import TVSI
import multiprocessing
import pandas as pd
# path = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/TVSI/Financial/Quarter/BalanceSheet/'
PATH = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/TVSI/Financial/Quarter/IncomeStatement/'

def finan(symbol):
    try:
        df = pd.read_csv(PATH+symbol+".csv")
    except:
        print(symbol,end=" ")
        com = TVSI.Financail(symbol=symbol)
        com.get_Income(2000,2022).to_csv(PATH+symbol+".csv",index=False)
        print(symbol,"Done!!!")

data = pd.read_excel("/content/List_Com_Phase1.xlsx")
Symbol = data["Symbol"]

def multip():
    pool = multiprocessing.Pool(processes=4)
    for symbol in Symbol:
        pool.apply_async(finan,args=(symbol,))
    pool.close()
    pool.join()

if __name__ == '__main__':
    multip()

