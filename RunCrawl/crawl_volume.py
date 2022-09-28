from ..Crawl import CafeF
from ..Crawl import VietStock
import pandas as pd
from ..Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV()
start = PATH_.DateCurrent - datetime.timedelta(days=180)
start = start.strftime("%d/%m/%Y")
end = PATH_.DateCurrent.strftime("%d/%m/%Y")


def VolumeCafeF(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/VolumeNow/{symbol}.csv")
    except:
        com = CafeF.Volume()
        com.getVolumeNow(symbol).to_csv(f"{PATH}/VolumeNow/{symbol}.csv",index=False)
        com.getVolumeEvent(symbol).to_csv(f"{PATH}/VolumeAdditionailEvents/{symbol}.csv",index=False)
    
# def VolumeVietStock(symbol):
#     PATH = PATH_.joinPath(PATH_.PATH_VOLUME,"VietStock")
#     try:
#         df = pd.read_csv(f"{PATH}/{symbol}.csv")
#     except:
#         com = VietStock.Other(symbol=symbol)
#         com.


List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    print(symbol)
    VolumeCafeF(symbol)