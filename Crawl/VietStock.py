import datetime
import time

from bs4 import BeautifulSoup
import pandas as pd
from Crawl.base.URL import URL_VIETSTOCK
from .base import setup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class FinanStatement(setup.Setup):
    '''
    Crawl Financial from VietStock
    '''
    def __init__(self,symbol):
        '''
        symbol: Mã Cổ phiếu 
        URL_BALANCED: link tài chính cân đối quý'''
        super().__init__(source="VS")
        self.symbol = symbol
    
    def setupLink(self):
        '''
        tạo lại link cho phù hợp với yêu cầu
        '''
        self.link_balance = URL_VIETSTOCK["BALANCE_SHEET"].replace("SYMBOL",self.symbol)
        self.link_income = URL_VIETSTOCK["INCOME_STATEMENT"].replace("SYMBOL",self.symbol)
        self.link_cashflow = URL_VIETSTOCK["CASH_FLOWS"].replace("SYMBOL",self.symbol)
    
    def get_FinancialReportPDF(self,symbol,year, cookie,data):
             
        rs = self.r_post(f"https://finance.vietstock.vn/data/getdocument",data=data,cookies=cookie,headers=self.headers)
        df = pd.DataFrame({"symbol":[],"year":[],"tilteVS":[],"LinkVS":[]})
        for row in rs.json():
            try:
                if self.check_new(row['FullName']):
                    df = df.append({"symbol":symbol,"year":year,"tilteVS":row['FullName'],"LinkVS":row['Url']},ignore_index=True)
            except:
                pass
        if df.empty:
            df = df.append({"symbol":symbol,"year":year,"tilteVS":"","LinkVS":""},ignore_index=True)
        return df
 
    def BalanceSheet(self,PeriodType):
        '''
        Lấy báo cáo tài chính cân đối
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm
        Output: DataFrame'''
        return self.table_lake(self.link_balance, PeriodType,True)

    def IncomStatement(self, PeriodType):
        '''
        Lấy báo cáo kết quả kinh doanh
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm
        Output: DataFrame'''
        return self.table_lake(self.link_income, PeriodType,False)

    def CashFlows(self, PeriodType):
        '''
        Lấy báo cáo lưu chuyển tiền tệ
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm
        Output: DataFrame'''
        return self.table_lake(self.link_cashflow, PeriodType,False)
    
    def table_lake(self, link, PeriodType,*arg):
        '''
        Lấy bảng dữ liệu
        Input: link: link
        PeriodType: 1: Quý, 2: 6 tháng, 4: năm
        Output: DataFrame'''
        self.request_link(link)
        self.click_to_all_year(PeriodType,*arg)
        data = self.getTable()
        return data

    def check_page(self):
        '''
        Kiểm tra trang có bị lỗi không
        Output: True: không bị lỗi, False: bị lỗi
        '''
        page_sourse = self.driver.page_source
        page = BeautifulSoup(page_sourse, "html.parser")
        check = page.find_all('div', {'class':'container m-b'})
        if len(check) == 0:
            return True

    def click_to_all_year(self, PeriodType,*arg):
        '''
        Chọn tất cả các năm
        Input: PeriodType: 1: Quý, 2: 6 tháng, 4: năm
        Output: DataFrame
        '''
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
        '''
        Lấy dữ liệu từ bảng
        Output: DataFrame 
        '''
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
    
    def clickInit(self,str_symbol,checkClick,type_time):
        '''
        Click vào các nút để lấy dữ liệu
        Input: 
            str_symbol: chuỗi các mã cổ phiếu
            checkClick: 
                True: có click, 
                False: không click 
            type_time: 
                1: Quý 1, 
                2: Quý 2, 
                3: Quý 3
                4: Quý 4
        Output: DataFrame 
        '''
        try: # turn off ad
            wait = WebDriverWait(self.driver, 10)
            close_btn_ele = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[9]/div[2]/div/div/div/div[1]/button")))

            close_btn_ele.click()
        except:
            pass
        self.click_something_by_id("txt-search-code")
        element = self.find_element_by_other("txt-search-code",By.ID)
        element.clear()
        self.send_something_by_id("txt-search-code",str_symbol)

        if checkClick:
            checkbox_xpaths = {
                "Quý 1": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[1]/label/input',
                "Quý 2": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[2]/label/input',
                "Quý 3": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[3]/label/input',
                "Quý 4": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[1]/td[4]/label/input',
                "6 tháng": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[2]/label/input',
                "9 tháng": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[1]/label/input',
                "Năm": '//*[@id="group-option-multi"]/div[2]/table/tbody/tr[2]/td[3]/label/input' 
            }

            selected_checkboxes = []
            if type_time == 1: # Nếu chọn quý 1
                selected_checkboxes.append("Quý 1")
            elif type_time == 2: # Nếu chọn quý 2
                selected_checkboxes.append("Quý 2")
            elif type_time == 3: # Nếu chọn quý 3
                selected_checkboxes.append("Quý 3")
            elif type_time == 4: # Nếu chọn quý 4
                selected_checkboxes.append("Quý 4")
            else: # Nếu chọn cả năm
                selected_checkboxes.append("Năm")

            dict_checkbox = {}
            for k in checkbox_xpaths.keys():
                dict_checkbox[k] = self.driver.find_element(by=By.XPATH, value=checkbox_xpaths[k])

            for k in dict_checkbox.keys():
                if k in selected_checkboxes:
                    if not dict_checkbox[k].is_selected():
                        dict_checkbox[k].click()
                else:
                    if dict_checkbox[k].is_selected():
                        dict_checkbox[k].click()
        self.click_something_by_other(".div-statement-button > .btn",By.CSS_SELECTOR)
        time.sleep(60)

    def CrawlWithBatch(self,list_symbol,type_time,PATH):
        '''
            Crawl dữ liệu với nhiều mã cổ phiếu 
            Input: 
                list_symbol: danh sách các mã cổ phiếu
                type_time: 1: Quý, 2: 6 tháng, 3:  4: năm
                PATH: đường dẫn lưu file
            Output: DataFrame
        '''

        self.request_link("https://finance.vietstock.vn/truy-xuat-du-lieu/bao-cao-tai-chinh.htm")
        checkClick = True
        for i in range(0,len(list_symbol),50):
            str_symbol = ",".join(list_symbol[i:i+50])
            self.clickInit(str_symbol,checkClick,type_time)
            checkClick = False
            page_sourse = self.driver.page_source
            page = BeautifulSoup(page_sourse, "html.parser")
            list_table = page.find_all(
                "table", {"class": "table table-striped table-hover"})
            data = pd.read_html(str(list_table))
            try:
                data = pd.concat([data[0], data[1]])
            except:
                data = data[0]
            data.to_csv(f'{PATH}/{i}.csv',index=False)
        return

class Other(setup.Setup):
    '''
    Crawl Other from VietStock
    '''
    def __init__(self) -> None:
        # super().__init__("Selenium")
        super().__init__(type_tech = "Selenium",source="VS")
        self.list_symbol_listing = pd.DataFrame({})
        self.time_end = datetime.datetime.today()
        self.time_start = self.time_end - datetime.timedelta(days=160)


    def CreateLink(self,type_,symbol=""):
        '''
        Tạo link cho phù hợp với yêu cầu
        Input: 
        type_: loại link 
        symbol: mã cổ phiếu'''
        return  URL_VIETSTOCK[type_].replace("SYMBOL",symbol)

    def CashDividend(self, symbol):
        '''
        Lấy thông tin cổ tức bằng tiền mặt
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.getTable(self.CreateLink('CASH_DIVIDEND',symbol))

    def BonusShare(self, symbol):
        '''
        Lấy thông tin thưởng cổ phiếu
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.getTable(self.CreateLink('BONUS_SHARE',symbol))

    def StockDividend(self, symbol):
        '''
        Lấy thông tin cổ tức bằng cổ phiếu
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.getTable(self.CreateLink('STOCK_DIVIDEND',symbol))

    def AdditionalListing(self, symbol):
        '''
        Lấy thông tin niêm yết bổ sung
        Input: symbol: mã cổ phiếu
        Output: DataFrame
        '''
        return self.getTable(self.CreateLink('ADDITIONAL_LISTING',symbol))
    
    def TreasuryStockTransactions(self, symbol):
        '''
        Lấy thông tin giao dịch cổ phiếu quỹ
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.getTable(self.CreateLink('TREASURY_STOCK_TRANSACTIONS',symbol))

    def VolumeNow(self,symbol):
        '''
        Lấy thông tin khối lượng giao dịch hiện tại
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.download_batch_get_request(self.CreateLink('LIST_INFOR',symbol),{"class":"table table-hover"})


    def Company_delisting(self, symbol):
        '''
        Lấy thông tin hủy niêm yết
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        return self.getTable(self.CreateLink('COMPANY_DELISTING',symbol))

    def Listing(self):
        '''
        Lấy thông tin niêm yết
        Output: DataFrame
        '''
        data_1 = self.getTableForListing(self.CreateLink('LISTING'),"1")
        data_2 = self.getTableForListing(self.CreateLink('LISTING'),"2")
        data_3 = self.getTableForListing(self.CreateLink('LISTING'),"5")
        data = pd.concat([data_1,data_2],ignore_index=True)
        data = pd.concat([data,data_3],ignore_index=True)
        return data
    def Delisting(self):
        '''
        Lấy thông tin hủy niêm yết
        Output: DataFrame
        '''
        return self.getTable(self.CreateLink('DELISTING'))
    
    def DividendPart(self,part_dividend):
        '''
        Lấy thông tin cổ tức
        Input: part_dividend: loại cổ tức
        Output: DataFrame'''
        self.request_link(URL_VIETSTOCK[part_dividend])
        start_txt = self.time_start.strftime("%d/%m/%Y")
        end_txt = self.time_end.strftime("%d/%m/%Y")
        self.send_something_by_other(start_txt,'//*[@id="txtFromDate"]/input',By.XPATH)
        self.send_something_by_other(end_txt,'//*[@id="txtToDate"]/input',By.XPATH)
        self.click_something_by_xpath('//*[@id="event-calendar-content"]/div/div[3]/div/button')
        time.sleep(2)
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

    def Dividend(self):
        '''
        Lấy thông tin cổ tức
        Output: DataFrame'''
        df1 = self.DividendPart("CASH_DIVIDEND")
        df1["Loại Sự kiện"] = ["Trả cổ tức bằng tiền mặt" for i in df1.index]
        df2 = self.DividendPart("BONUS_SHARE")
        df2["Loại Sự kiện"] = ["Thưởng cổ phiếu" for i in df2.index]
        df3 = self.DividendPart("STOCK_DIVIDEND")
        df3["Loại Sự kiện"] = ["Trả cổ tức bằng cổ phiếu" for i in df3.index]
        df = pd.concat([df1,df2,df3],ignore_index=True)
        return df

    def getTable(self, link):
        '''
        Lấy bảng dữ liệu
        Input: link: link
        Output: DataFrame'''
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
        '''
        Chọn sàn
        Input: exchange: sàn
        Output: DataFrame'''
        self.click_select("exchange",exchange)
        self.click_select("businessTypeID","1")
        self.click_something_by_xpath('//*[@id="corporate-az"]/div/div[1]/div[1]/button')
        time.sleep(2)

    def getTableForListing(self, link,exchange):
        '''
        Lấy bảng dữ liệu
        Input: link: link
        Output: DataFrame'''
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
        '''
        Lấy bảng dữ liệu
        Output: DataFrame
        '''
        self.click_something_by_id('btn-page-next')
        time.sleep(5)
        page = BeautifulSoup(self.driver.page_source, 'html.parser')
        return self.getTableInfor(page)

    def getTableInfor(self, page):
        '''
        Lấy bảng dữ liệu
        Output: DataFrame'''
        time.sleep(1)
        list_table = page.find_all('table', {'class':
        'table table-striped table-bordered table-hover table-middle pos-relative m-b'})
        try: return pd.read_html(str(list_table))[0]
        except: return pd.DataFrame(columns=[i.text for i in list_table])
            
    def getNumberPage(self, page):
        '''
        Lấy số trang
        Output: int'''
        try:number_pages=int(page.find_all('span', {'class':'m-r-xs'})[1].find_all('span')[1].text)
        except: number_pages=0
        return int(number_pages)

    def lst_infor(self, symbol):
        '''
        Lấy thông tin cơ bản
        Input: symbol: mã cổ phiếu
        Output: DataFrame'''
        self.request_link(self.CreateLink("LIST_INFOR",symbol))
        return self.getTableInforcom()

    def getTableInforcom(self):
        '''
        Lấy bảng dữ liệu
        Output: DataFrame'''

        page_source = self.driver.page_source
        page = BeautifulSoup(page_source, 'html.parser')
        list_table = page.find_all('table', {'class':'table table-hover'})
        if len(list_table) == 0: 
            return pd.DataFrame({'Nothing':[]})
        return pd.read_html(str(list_table))[0]
    
    
  