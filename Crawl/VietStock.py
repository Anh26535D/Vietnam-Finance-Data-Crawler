import time

from bs4 import BeautifulSoup
import pandas as pd
from Crawl.base.URL import URL_VIETSTOCK
from .base import setup

class FinanStatement(setup.Setup):
    def __init__(self,symbol):
        super().__init__()
        self.symbol = symbol
    
    def setupLink(self):
        self.link_balance = URL_VIETSTOCK["BALANCE_SHEET"].replace("SYMBOL",self.symbol)
        self.link_income = URL_VIETSTOCK["INCOME_STATEMENT"].replace("SYMBOL",self.symbol)
        self.link_cashflow = URL_VIETSTOCK["CASH_FLOWS"].replace("SYMBOL",self.symbol)
        
    def BalanceSheet(self,PeriodType):
        return self.table_lake(self.link_balance, PeriodType,True)

    def IncomStatement(self, PeriodType):
        return self.table_lake(self.link_income, PeriodType,False)

    def CashFlows(self, PeriodType):
        return self.table_lake(self.link_cashflow, PeriodType,False)
    
    def table_lake(self, link, PeriodType,*arg):
        self.request_link(link)
        self.click_to_all_year(PeriodType,*arg)
        data = self.getTable()
        return data

    def check_page(self):
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        check = page.find_all('div', {'class':'container m-b'})
        if len(check) == 0:
            return True

    def click_to_all_year(self, PeriodType,*arg):
        try:
            try:
                self.click_select("period","2")
                time.sleep(0.5)
                self.click_select("UnitDong","1000")
                time.sleep(0.5)
                self.click_select("PeriodType",PeriodType)
                time.sleep(0.5)
            except: pass
            if arg[0] != False:
                try:
                    self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]')
                    time.sleep(0.5)
                    self.click_something_by_xpath('//*[@id="expand-overall-CDKT"]')
                    time.sleep(1)
                except: pass
        except:
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
    def __init__(self) -> None:
        super().__init__()
        self.list_symbol_listing = pd.DataFrame({})

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

    def VolumeNow(self,symbol):
        return self.download_batch_get_request(self.CreateLink('LIST_INFOR',symbol),{"class":"table table-hover"})


    def Company_delisting(self, symbol):
        return self.getTable(self.CreateLink('COMPANY_DELISTING',symbol))

    def Listing(self):
            data_1 = self.getTableForListing(self.CreateLink('LISTING'),"1")
            data_2 = self.getTableForListing(self.CreateLink('LISTING'),"2")
            data_3 = self.getTableForListing(self.CreateLink('LISTING'),"5")
            data = pd.concat([data_1,data_2],ignore_index=True)
            data = pd.concat([data,data_3],ignore_index=True)
            return data
    def Delisting(self):
        return self.getTable(self.CreateLink('DELISTING'))

    def getTable(self, link):
        self.request_link(link)
        time.sleep(1)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        if number_pages > 1:
            data = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                data_new = self.getNextTable()
                data= pd.concat([data, data_new])
            return data
        return self.getTableInfor(page)
    
    def getExchangeNormal(self,exchange):
        self.click_select("exchange",exchange)
        self.click_select("businessTypeID","1")
        self.click_something_by_xpath('//*[@id="corporate-az"]/div/div[1]/div[1]/button')
        time.sleep(2)

    def getTableForListing(self, link,exchange):
        self.request_link(link)
        time.sleep(1)
        self.getExchangeNormal(exchange)
        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        number_pages = self.getNumberPage(page)
        if number_pages > 1:
            # if self.list_symbol_listing.empty:
            self.list_symbol_listing = self.getTableInfor(page)
            for number_page in range(2, number_pages+1):
                data_new = self.getNextTable()
                self.list_symbol_listing= pd.concat([self.list_symbol_listing, data_new])
            return self.list_symbol_listing
        else: return self.getTableInfor(page)
    
    def getNextTable(self):
        self.click_something_by_id('btn-page-next')
        time.sleep(2)
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