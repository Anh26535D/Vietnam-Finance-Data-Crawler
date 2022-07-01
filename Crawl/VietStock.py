import time

from bs4 import BeautifulSoup
import pandas as pd
from Crawl.base.URL import URL_VIETSTOCK
from .base import setup

class FinanStatement(setup.Setup):
    def __init__(self,symbol):
        super().__init__()
        self.symbol = symbol
        self.link_balance = URL_VIETSTOCK["BALANCE_SHEET"].replace("SYMBOL",symbol)
        self.link_income = URL_VIETSTOCK["INCOME_STATEMENT"].replace("SYMBOL",symbol)
        self.link_cashflow = URL_VIETSTOCK["CASH_FLOWS"].replace("SYMBOL",symbol)


    def BalanceSheet(self,PeriodType):
        return self.table_lake(self.link_balance, PeriodType)

    def IncomStatement(self, PeriodType):
        return self.table_lake(self.link_income, PeriodType)

    def CashFlows(self, PeriodType):
        return self.table_lake(self.link_cashflow, PeriodType)
    
    def table_lake(self, link, PeriodType):
        self.request_link(link)
        if self.check_page() == True:
            self.click_to_all_year(PeriodType)
            time.sleep(1)
            data = self.getTable()
        else: data = pd.DataFrame({'Nothing':[]})
        return data

    def check_page(self):
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        check = page.find_all('div', {'class':'container m-b'})
        if len(check) == 0:
            return True

    def click_to_all_year(self, PeriodType):
        try:
            try:
                self.click_select("period","-1")
                time.sleep(0.5)
                self.click_select("UnitDong","1000")
                time.sleep(0.5)
                self.click_select("PeriodType",PeriodType)
                time.sleep(2)
            except: pass
            try:
                self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]/i')
                time.sleep(2)
                self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]/i')
                time.sleep(0.3)
            except: pass
        finally:
            pass

    def getTable(self):
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        list_table = page.find_all(
            "table", {"class": "table table-hover"})
        try:
            data = pd.read_html(str(list_table))
            try:
                data = pd.concat([data[0], data[1]])
            except:
                data = data[0]
        except:
            data = pd.DataFrame({'Nothing':[]})
        return data

class Other(setup.Setup):
    def __init__(self,symbol) -> None:
        super().__init__()

    def CreateLink(self,type_,symbol=""):
        return  URL_VIETSTOCK[type_].replace("SYMBOL",symbol)

    def CashDividend(self, symbol):
        return self.getTable(self.CreateLink('CASH_DIVIDEND',symbol))

    def BonusShare(self, symbol):
        return self.getTable(self.CreateLink('BONUS_SHARE',symbol))

    def StockDividend(self, symbol):
        return self.getTable(self.CreateLink('STOCK_DIVIDEND',symbol))

    def AdditionalListing(self, symbol):
        return self.getTable(self.CreateLink('ADDITIONAL_LISTING',symbol))
    
    def TreasuryStockTransactions(self, symbol):
        return self.getTable(self.CreateLink('TREASURY_STOCK_TRANSACTIONS',symbol))

    def Company_delisting(self, symbol):
        return self.getTable(self.CreateLink('COMPANY_DELISTING',symbol))
    
    def Listing(self):
        return self.getTable(self.CreateLink('LISTING'))
    def Delisting(self):
        return self.getTable(self.CreateLink('DELISTING'))
    def getTable(self, link):
        self.request_link(link)
        time.sleep(1)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        # print(number_pages)
        if number_pages > 1:
            data = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                # if method == 'number_page'
                data_new = self.getNextTable(number_page, link)
                data= pd.concat([data, data_new])
            return data
        else: return self.getTableInfor(page)

    def getNextTable(self):
        self.click_something_by_id('btn-page-next')
        time.sleep(1)
        page = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self.getTableInfor(page)

    def getTableInfor(self, page):
        time.sleep(1)
        list_table = page.find_all('table', {'class':
        'table table-striped table-bordered table-hover table-middle pos-relative m-b'})
        try: return pd.read_html(str(list_table))[0]
        except: return pd.DataFrame(columns=[i.text for i in list_table])
            
    def getNumberPage(self, page):
        try:number_pages = int(page.find_all('span', {'class':'m-r-xs'})[1].find_all('span')[1].text)
        except: number_pages = 0
        return int(number_pages)

    def lst_infor(self, symbol):
        self.request_link(self.CreateLink("LIST_INFOR",symbol))
        return self.getTableInforcom()

    def getTableInforcom(self):
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        list_table = page.find_all('table', {'class':'table table-hover'})
        if len(list_table) == 0: 
            return pd.DataFrame({'Nothing':[]})
        return pd.read_html(str(list_table))[0]