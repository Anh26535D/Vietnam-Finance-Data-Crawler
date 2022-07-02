from Crawl import TVSI
import multiprocessing
path = '/content/drive/MyDrive/Data Lake/Ingestion/Day 0/TVSI/Financial/Quarter/BalanceSheet/'
symbol = "AAA"
com = TVSI.Financail(symbol=symbol)
com.get_Balance(2000,2022).to_csv(symbol+".csv")
