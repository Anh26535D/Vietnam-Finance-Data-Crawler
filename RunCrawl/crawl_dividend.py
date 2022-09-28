from ..Crawl import CafeF
from ..Crawl import VietStock
import pandas as pd
from ..Flow import PATH_env
import datetime

PATH_ = PATH_env.PATH_ENV()
start = PATH_.DateCurrent - datetime.timedelta(days=180)
start = start.strftime("%d/%m/%Y")
end = PATH_.DateCurrent.strftime("%d/%m/%Y")


def DividendCafeF(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_DIVIDEND,"CafeF")
    try:
        df = pd.read_csv(f"{PATH}/{symbol}.csv")
    except:
        try:
            com = CafeF.Dividend()
            com.get_new(symbol).to_csv(f"{PATH}/{symbol}.csv",index=False)
        except:
            pass
        
def DividendVietStock(symbol):
    PATH = PATH_.joinPath(PATH_.PATH_DIVIDEND,"VietStock")
    try:
        df = pd.read_csv(f"{PATH}/BonusShare/{symbol}.csv")
    except:
        try:
            com = VietStock.Other(symbol=symbol)
            com.BonusShare(symbol).to_csv(f"{PATH}/BonusShare/{symbol}.csv",index=False)
            com.CashDividend(symbol).to_csv(f"{PATH}/CashDividend/{symbol}.csv",index=False)
            com.StockDividend(symbol).to_csv(f"{PATH}/StockDividend/{symbol}.csv",index=False)
        except:
            pass
       

List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    try:
        print(symbol)
        DividendCafeF(symbol)
        DividendVietStock(symbol)
