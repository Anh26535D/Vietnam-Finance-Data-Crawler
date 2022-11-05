import sys
sys.path.append(r'C:\DataVietNam')
from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env,RUN
import datetime
import time
import json

PATH_ = PATH_env.PATH_ENV("Ingestion")
start = PATH_.DateCurrent - datetime.timedelta(days=90)

def checkfile(symbol,file_type):
    try:
        with open(f"{PATH}/{file_type}/{symbol}.json", 'r',encoding='utf-8') as j:
            temp = json.loads(j.read())
    except:
        try:
            pd.read_csv(f"{PATH}/{file_type}/{symbol}.csv")
        except:
            return False
    return True

def test_data(symbol):
  if checkfile(symbol,"IncomeStatement")==False:
      yield 1
  if checkfile(symbol,"BalanceSheet")==False:
      yield 2
  if checkfile(symbol,"CashFlowInDirect")==False:
    yield 3
  if checkfile(symbol,"CashFlowDirect")==False:
    yield 4

dict_time = {
    "Q":"Quarter/",
    "Y":"Year/",
    "QUY":"Quarter/",
    "NAM":"Year/"
}


def FinancialCafeF(symbol,type_):
    global PATH
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"CafeF",dict_time[type_])
    list_must_crawl_again = list(test_data(symbol))
    if len(list_must_crawl_again) == 0:
        return 0
    else:
        print(symbol,list_must_crawl_again,end=" ")
    web = CafeF.FinancailStatement()
    time = 3
    for i in list_must_crawl_again:
        if i == 1:
            income = web.get_Income(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}IncomeStatement/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(income, outfile, ensure_ascii=False)
        elif i == 2:
            balan = web.get_Balance(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}BalanceSheet/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(balan, outfile, ensure_ascii=False)
        elif i == 3:
            CFID = web.get_CashFlowIndirect(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowInDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFID, outfile, ensure_ascii=False)
        elif i == 4:
            CFD = web.get_CashFlowDirect(symbol, year=start.year,month=start.month,day=start.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFD, outfile, ensure_ascii=False)
        else:
            print("loi nang, dell lap trinh nua")
    print("Done CF!!",symbol)
    web.turn_off_drive()

webVS = VietStock.FinanStatement("")
webVS.login_VS()

def FinancialVietStock(symbol,type_):
    global PATH
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"VietStock",dict_time[type_])
    list_must_crawl_again = list(test_data(symbol))
    if len(list_must_crawl_again) == 0:
        return 0
    else:
        print(symbol,list_must_crawl_again,end=" ")
    # list_must_crawl_again = [1,2,3,4]
    webVS.symbol=symbol
    webVS.setupLink()
    for i in list_must_crawl_again:
        if i == 1:
            # pass
            income = webVS.IncomStatement(type_)
            income.to_csv(f"{PATH}IncomeStatement/{symbol}.csv",index=False)
        elif i == 2:
            # pass
            balan = webVS.BalanceSheet(type_)
            balan.to_csv(f"{PATH}BalanceSheet/{symbol}.csv",index=False)
        elif i == 3:
            CFID = webVS.CashFlows(type_)
            CFID.to_csv(f"{PATH}CashFlowInDirect/{symbol}.csv",index=False)
        elif i == 4:
            pass
        else:
            print("loi nang, dell lap trinh nua")
    print("Done VS!!",symbol)

def run_reset_cf():
    # global web
    # try:
    #     # web = CafeF.FinancailStatement()
    # except:
    #     print("Tam Nghi CF-------------------")
    # time.sleep(20)
    #     run_reset_cf()
    pass
        
def run_reset_vs():
    global webVS
    try:
        webVS = VietStock.FinanStatement("")
        webVS.login_VS()
    except:
        print("Tam Nghi VS-------------------")
        time.sleep(10)
        run_reset_vs()


# List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
# List_Symbol = pd.read_excel('G:/My Drive/DataVIS/VietNam/Data Lake/Raw_VIS/2022-10-21/Compare/Financial_Quarter_CheckList.xlsx')
# SYMBOL = List_Symbol[List_Symbol["VietStock"] == False]["Symbol"].values
for symbol in SYMBOL:
    try:
        FinancialCafeF(symbol,"Q")
    except:
        run_reset_cf()

    # try:
    #     FinancialCafeF(symbol,"Y")
    # except:
    #     run_reset_cf()

    # try:
    #     FinancialVietStock(symbol,"NAM")
    # except:
    #     run_reset_vs()
    print(symbol)
    try:
        FinancialVietStock(symbol,"QUY")
    except:
        run_reset_vs()
webVS.turn_off_drive()

# #     break