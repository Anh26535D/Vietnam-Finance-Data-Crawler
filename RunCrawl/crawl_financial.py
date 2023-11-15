import sys
sys.path.append(r'E:\vis\vis_vietnamese_data\DataVietNam')


from Crawl import CafeF
from Crawl import VietStock
import pandas as pd
from Flow import PATH_env
import datetime
import time
import json


PATH_ = PATH_env.PATH_ENV("Ingestion")
start_date = PATH_.DateCurrent - datetime.timedelta(days=90)
y = start_date.year

if start_date.month in [1,2,3]:
    q = 1
elif start_date.month in [4,5,6]:
    q = 2
elif start_date.month in [7,8,9]:
    q = 3
elif start_date.month in [10,11,12]:
    q = 4

time_formats = {
    "Q":"Quarter/",
    "Y":"Year/",
    "QUY":"Quarter/",
    "NAM":"Year/"
}

webVS = VietStock.FinanStatement("")
webVS.login_VS()

def check_file_existence(symbol, document_type):
    '''
    Check the existence of a file.

    Parameters
    ----------
    symbol : str
        Stock symbol.
    document_type : str
        Document type.

    Returns
    -------
    bool
        Returns True if the file exists; otherwise, returns False.
    '''
    
    try:
        with open(f"{PATH}/{document_type}/{symbol}.json", 'r', encoding='utf-8') as j:
            temp_data = json.loads(j.read())
    except:
        try:
            temp_data = pd.read_csv(f"{PATH}/{document_type}/{symbol}.csv")
        except:
            return False
    return True


def check_crawled_data(symbol):
    '''
    Check if financial data has been crawled for the given stock symbol.

    Parameters
    ----------
    symbol : str
        Stock symbol.

    Yields
    -------
    int
        Yields integers corresponding to uncrawled data types:
        1 - Income Statement
        2 - Balance Sheet
        3 - Cash Flow (Indirect Method)
        4 - Cash Flow (Direct Method)
    '''
    
    if not check_file_existence(symbol, "IncomeStatement"):
        yield 1
    if not check_file_existence(symbol, "BalanceSheet"):
        yield 2
    if not check_file_existence(symbol, "CashFlowInDirect"):
        yield 3
    if not check_file_existence(symbol, "CashFlowDirect"):
        yield 4


def FinancialCafeF(symbol, type_):
    '''
    Fetches financial data from CafeF website and saves it as JSON files.

    Parameters
    ----------
    symbol : str
        Stock symbol.
    data_type : str
        Type of financial data to fetch (e.g., "Q" for quarterly, "Y" for yearly).
    '''

    global PATH

    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL, "CafeF", time_formats[type_])
    uncrawled_data_types = list(check_crawled_data(symbol))

    if len(uncrawled_data_types) == 0:
        return 0

    print(symbol, uncrawled_data_types, end=" ")

    web = CafeF.FinancialStatement()
    time = 3
    for i in uncrawled_data_types:
        if i == 1:
            income_data = web.get_Income(
                symbol, year=start_date.year, month=start_date.month, day=start_date.day, type_=type_, times=time)
            with open(f"{PATH}IncomeStatement/{symbol}.json", "w", encoding='utf8') as outfile:
                json.dump(income_data, outfile, ensure_ascii=False)
        elif i == 2:
            balance_sheet_data = web.get_Balance(
                symbol, year=start_date.year, month=start_date.month, day=start_date.day, type_=type_, times=time)
            with open(f"{PATH}BalanceSheet/{symbol}.json", "w", encoding='utf8') as outfile:
                json.dump(balance_sheet_data, outfile, ensure_ascii=False)
        elif i == 3:
            cash_flow_indirect_data = web.get_CashFlowIndirect(
                symbol, year=start_date.year, month=start_date.month, day=start_date.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowInDirect/{symbol}.json", "w", encoding='utf8') as outfile:
                json.dump(cash_flow_indirect_data, outfile, ensure_ascii=False)
        elif i == 4:
            cash_flow_direct_data = web.get_CashFlowDirect(
                symbol, year=start_date.year, month=start_date.month, day=start_date.day, type_=type_, times=time)
            with open(f"{PATH}CashFlowDirect/{symbol}.json", "w", encoding='utf8') as outfile:
                json.dump(cash_flow_direct_data, outfile, ensure_ascii=False)
        else:
            print("Error: Invalid data type encountered during data retrieval.")

    print(f"Done fetching financial data for {symbol}")
    web.turn_off_drive()


def FinancialVietStock(symbol, type_):
    '''
    Fetches financial data from VietStock website and saves it as CSV files.
    
    Parameters
    ----------
    symbol : str
        Stock symbol.
    data_type : str
        Type of financial data to fetch (e.g., "Q" for quarterly, "Y" for yearly).
    '''

    global PATH

    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL, "VietStock", time_formats[type_])
    uncrawled_data_types = list(check_crawled_data(symbol))

    if len(uncrawled_data_types) == 0:
        return 0

    print(symbol,uncrawled_data_types,end=" ")

    webVS.symbol = symbol
    webVS.setupLink()
    for i in uncrawled_data_types:
        if i == 1:
            income_statement = webVS.IncomStatement(type_)
            income_statement.to_csv(
                f"{PATH}IncomeStatement/{symbol}.csv", index=False)
        elif i == 2:
            balance_sheet = webVS.BalanceSheet(type_)
            balance_sheet.to_csv(
                f"{PATH}BalanceSheet/{symbol}.csv", index=False)
        elif i == 3:
            cash_flow_indirect = webVS.CashFlows(type_)
            cash_flow_indirect.to_csv(
                f"{PATH}CashFlowInDirect/{symbol}.csv", index=False)
        elif i == 4:
            pass
        else:
            print("Error: Invalid data type encountered during data retrieval.")
    print(f"Done fetching financial data for {symbol}")


def run_reset_cf():
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


def update_stock_symbols_status(stock_symbols, **kwargs):
    '''
    Updates the status of stock symbols in the given list.

    Parameters
    ----------
    stock_symbols : dict
        Dictionary containing stock symbols as keys and their statuses as values.

    Returns
    -------
    dict
        Updated dictionary of stock symbols with their statuses.
    '''

    for key,value in kwargs.items():
        stock_symbols[key] = value

    return stock_symbols

def run_crawl(func_crawl, func_reset, symbol, type_, state):
    '''
    Executes the crawling process.

    Parameters
    ----------
    func_crawl : function
        Function to crawl financial data.
    func_reset : function
        Function to reset the crawl state.
    symbol : str
        Stock symbol.
    data_type : str
        Type of financial data to crawl.
    state : bool
        Crawl state (True for successfully crawled, False for failed crawl).

    Returns
    -------
    bool
        True if crawl is successful, False otherwise.
    '''
    
    if state:
        return True
    try:
        func_crawl(symbol, type_)
        return True
    except:
        func_reset()
        return False


list_symbol_df = pd.read_csv(
    f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
initial_status = [False for _ in list_symbol_df.index]
list_symbol_df = update_stock_symbols_status(
    list_symbol_df, VS_Q=initial_status, VS_Y=initial_status)
list_symbol_df.to_csv(
    f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv', index=False)


for i in range(3):
    list_symbol_df = pd.read_csv(
        f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
    CheckStateVS_QUARTER = []
    CheckStateVS_YEAR = []

    PATH = PATH_.joinPath(PATH_.PATH_FINANCIAL, "VietStock")

    webVS.CrawlWithBatch(list_symbol_df["Mã CK▲"], q, f"{PATH}/Quarter")
    webVS.CrawlWithBatch(list_symbol_df["Mã CK▲"], y, f"{PATH}/Year")

    for idx in list_symbol_df.index:
        state_VS_Q, state_VS_Y = list_symbol_df["VS_Q"][idx], list_symbol_df["VS_Y"][idx]
        symbol = list_symbol_df["Mã CK▲"][idx]
        state_VS_Q = run_crawl(FinancialVietStock,run_reset_vs,symbol,"QUY",state_VS_Q)
        state_VS_Y = run_crawl(FinancialVietStock,run_reset_vs,symbol,"NAM",state_VS_Y)
        
        CheckStateVS_QUARTER.append(state_VS_Q)
        CheckStateVS_YEAR.append(state_VS_Y)
    list_symbol_df = update_stock_symbols_status(
        list_symbol_df, VS_Q=CheckStateVS_QUARTER, VS_Y=CheckStateVS_YEAR)
    list_symbol_df.to_csv(
        f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv', index=False)


webVS.turn_off_drive()