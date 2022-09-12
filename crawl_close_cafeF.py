from Crawl import TVSI
from Crawl import StockBiz
import pandas as pd


# def closeCafeF(symbol):
#     try:
#         df = pd.read_csv(PATH_env+symbol+".csv")
#     except:
#         com = StockBiz.Close(symbol=symbol)
#         com.DownloadClose().to_csv(f"{PATH_env}{symbol}.csv")

# def close(symbol):
#     try:
#         df = pd.read_csv(PATH_env+symbol+".csv")
#     except:
#         com = StockBiz.Close(symbol=symbol)
#         com.DownloadClose().to_csv(f"{PATH_env}{symbol}.csv")