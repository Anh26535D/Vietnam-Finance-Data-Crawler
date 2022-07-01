from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import requests
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from Crawl.base.URL import URL_VIETSTOCK, USER,PASSWORD
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
pd.set_option('mode.chained_assignment', None)

class Setup():
    def __init__(self) -> None:
        self.user = USER
        self.password = PASSWORD
        self.year = 0
        self.quater = 0
        self.day = 0
        self.symbol = ""
        self.form_data = {}
        self.VS = URL_VIETSTOCK["LOGIN"] 
        self.HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
        try:
            self.reset_driver()
        except:
            self.reset_colab()

    def reset_colab(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('enable-automation')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    def reset_driver(self, path="C:/webdrive/chromedriver.exe"):
        self.driver = webdriver.Chrome(executable_path=path)

    def request_link(self,link,time=5):
        try:
            self.driver.set_page_load_timeout(time)
            self.driver.get(link)
        except:
            self.request_link(link,10)

    def format(self, time):
        s = time.split("-")
        self.year = int(s[0])
        self.quater = int(s[1])//3+1
        self.day = int(s[2])
        return self.year, self.quater

    def find_element_by_xpath(self,something):
        try:
          element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,something)))
        finally:
            pass
        return element

    def click_something_by_xpath(self, something):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, something))
            )
            element.click()
        except:
            self.driver.refresh()
            pass

    def click_something_by_id(self, something):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, something))
            )
            element.click()
        except:
            self.driver.refresh()
            pass
    def send_something_by_id(self,id,somthing):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )
            element.send_keys(somthing)
        except:
            self.driver.refresh()
            pass


    def click_select(self,name,value):
        select = Select(self.driver.find_element_by_name(name))
        select.select_by_value(value)
        

    def download_batch_get_post(self,url,dict_={}):
        rs = requests.post(url, data = self.form_data, headers = self.HEADERS)
        soup = BeautifulSoup(rs.content, 'html.parser')
        table = soup.find('table',dict_)
        stock_slice_batch = pd.read_html(str(table))[0]
        return stock_slice_batch
    
    def download_batch_selenium(self,url,dict_={}):
        self.request_link(url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find('table',dict_)
        stock_slice_batch = pd.read_html(str(table))[0]
        return stock_slice_batch

    def download_batch_get_request(self,url,dict_={}):
        rs = requests.get(url, headers = self.HEADERS)
        soup = BeautifulSoup(rs.content, 'html.parser')
        table = soup.find_all('table',dict_)
        stock_slice_batch = pd.read_html(str(table))[0]
        return stock_slice_batch
    
    def login_VS(self):
        self.driver.get(self.VS)
        self.driver.maximize_window() 
        try:       
            self.click_something_by_id('btn-request-call-login')
            self.send_something_by_id('txtEmailLogin',self.user)
            self.send_something_by_id('txtPassword',self.password)
            self.click_something_by_id('btnLoginAccount')
        finally:
            time.sleep(1)
            pass