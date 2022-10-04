import sys
import time
sys.path.append("C:\DataVietNam")

from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV("Ingestion")

def VolumeCafeF(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/VolumeNow/{symbol}.csv")
    except:
        com = CafeF.Volume()
        com.getVolumeNow(symbol).to_csv(f"{PATH}/VolumeNow/{symbol}.csv",index=False)
        com.getVolumeEvent(symbol).to_csv(f"{PATH}/VolumeAdditionailEvents/{symbol}.csv",index=False)
    
com = VietStock.Other()
def VolumeVietStock(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"VietStock")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        com.AdditionalListing(symbol).to_csv(f"{PATH}/VolumeAdditionailEvents/{symbol}.csv",index=False)
        com.VolumeNow(symbol).to_csv(f"{PATH}/VolumeNow/{symbol}.csv",index=False)
        com.TreasuryStockTransactions(symbol).to_csv(f"{PATH}/TreasuryShares/{symbol}.csv",index=False)

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    VolumeCafeF(symbol)
    VolumeVietStock(symbol)
    print("Done: ",symbol)
    