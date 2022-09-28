from ..Crawl import CafeF
from ..Crawl import VietStock
import pandas as pd
from ..Flow import PATH_env
import datetime
import json

PATH_ = PATH_env.PATH_ENV()
start = PATH_.DateCurrent - datetime.timedelta(days=180)
start = start.strftime("%d/%m/%Y")
end = PATH_.DateCurrent.strftime("%d/%m/%Y")

def checkfile(symbol,file_type):
  try:
    with open(f"{PATH}/{file_type}/{symbol}.json", 'r',encoding='utf-8') as j:
      temp = json.loads(j.read())
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
    time = 2
    for i in list_must_crawl_again:
        if i == 1:
            income = web.get_Income(symbol, year=PATH_.DateCurrent.year,month=PATH_.DateCurrent.month,day=PATH_.DateCurrent.day, type_=type_, times=time)
            with open(f"{PATH}IncomeStatement/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(income, outfile, ensure_ascii=False)
        elif i == 2:
            balan = web.get_Balance(symbol, year=PATH_.DateCurrent.year,month=PATH_.DateCurrent.month,day=PATH_.DateCurrent.day, type_=type_, times=time)
            with open(f"{PATH}BalanceSheet/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(balan, outfile, ensure_ascii=False)
        elif i == 3:
            CFID = web.get_CashFlowIndirect(symbol, year=PATH_.DateCurrent.year,month=PATH_.DateCurrent.month,day=PATH_.DateCurrent.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowInDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFID, outfile, ensure_ascii=False)
        elif i == 4:
            CFD = web.get_CashFlowDirect(symbol, year=PATH_.DateCurrent.year,month=PATH_.DateCurrent.month,day=PATH_.DateCurrent.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowDirect/{symbol}.json", "w",encoding='utf8') as outfile:
                    json.dump(CFD, outfile, ensure_ascii=False)
        else:
            print("loi nang, dell lap trinh nua")
    print("Done!!",symbol)



webVS = VietStock.FinanStatement("AAA")
webVS.login_VS()

def FinancialVietStock(symbol,type_):
    global PATH
    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL,"VietStock",dict_time[type_])
    list_must_crawl_again = list(test_data(symbol))
    if len(list_must_crawl_again) == 0:
        return 0
    else:
        print(symbol,list_must_crawl_again,end=" ")
    webVS.symbol=symbol
    webVS.setupLink()

    time = 2
    for i in list_must_crawl_again:
        if i == 1:
            income = webVS.IncomStatement(type_)
            income.to_csv(f"{PATH}IncomeStatement/{symbol}.csv",index=False)
        elif i == 2:
            balan = webVS.BalanceSheet(type_)
            balan.to_csv(f"{PATH}BalanceSheet/{symbol}.csv",index=False)
        elif i == 3:
            CFID = webVS.CashFlows(type_)
            CFID.to_csv(f"{PATH}CashFlowInDirect/{symbol}.csv",index=False)
        else:
            print("loi nang, dell lap trinh nua")
    print("Done!!",symbol)

def runVS(func):
    try:
        func
    except:
        webVS = VietStock.FinanStatement("")
        webVS.login_VS()
List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    FinancialCafeF(symbol,"Q")
    FinancialCafeF(symbol,"Y")
    runVS(FinancialVietStock(symbol,"NAM"))
    runVS(FinancialVietStock(symbol,"QUY"))
# #     break