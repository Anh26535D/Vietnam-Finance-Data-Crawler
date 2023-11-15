from .base import setup
import pandas as pd
import json
from datetime import datetime
import requests

import sys
import codecs

try:
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
except:
    pass


class Price(setup.Setup):
    """
    Crawl price from https://iboard.ssi.com.vn/"""

    def __init__(self, type_tech="") -> None:
        """
        type_tech: Selenium or Colab"""
        super().__init__(type_tech)

    def crawlPriceIBoard(self, exchange):
        """
        Crawl price from https://iboard.ssi.com.vn/
        """
        url = f"https://iboard-query.ssi.com.vn/stock/exchange/{exchange}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = json.loads(response.content)
        else:
            content = {"data": []}

        return content["data"]

    def getPriceToDayWithExchange(self, exchange="hose"):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên sàn bất kỳ
        Input:  exchange: hose, hnx, upcom
        output: DataFrame
        """
        date = datetime.now().strftime("%Y-%m-%d")
        data = self.crawlPriceIBoard(exchange)
        dict_ = {"Symbol": [], "Price": [], "Volume": []}

        for row in data["data"]["stockRealtimes"]:
            dict_["Symbol"].append(row["stockSymbol"])
            dict_["Price"].append(row["matchedPrice"])
            dict_["Volume"].append(row["nmTotalTradedQty"])
        dict_["Day"] = [date for i in dict_["Symbol"]]
        dict_["Exchange"] = [exchange.upper() for i in dict_["Symbol"]]
        return pd.DataFrame(dict_)

    def getIBoardExchange(self, exchange="hose"):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên sàn bất kỳ
        Input:  exchange: hose, hnx, upcom
        Output: DataFrame
        """
        data = self.crawlPriceIBoard(exchange)
        return pd.DataFrame(data)

    def getPriceToDayAllExchange(self):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên tất cả các sàn
        Output: DataFrame
        """
        exchange = ["hose", "hnx", "upcom"]
        result = pd.DataFrame()
        for ex in exchange:
            data = self.getPriceToDayWithExchange(ex)
            result = pd.concat([result, data], ignore_index=True)
        return result

    def getIBoardAllExchange(self):
        """
        Lấy giá ngày hôm nay của các mã chứng khoán trên tất cả các sàn
        Output: DataFrame

        """
        exchange = ["hose", "hnx", "upcom"]
        result = pd.DataFrame()
        for ex in exchange:
            data = self.getIBoardExchange(ex)
            result = pd.concat([result, data], ignore_index=True)
        return result
