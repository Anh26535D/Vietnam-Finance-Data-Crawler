import pandas as pd
import re

class Dividend():
    def __init__(self,dict_path_) -> None:
        self.path_object = dict_path_
        pass
    def Dividend_CF(self,symbol):
      list_ = []
      try:
        news = pd.read_csv({self.path_object["F0"]["Dividend"]}+symbol+".csv")
        for new in news["New"]:
            try:
                day = re.search(r'(\d+/\d+/\d+)',new).group(1)
                index_stock = new.find("Cổ tức bằng Cổ phiếu")
                index_money = new.find("Cổ tức bằng Tiền")
                scale,money = '-1','-1'
                if index_stock != -1:
                    scale = re.search(r'(\d+:\d+)',new[index_stock:]).group(1)
                if index_money != -1:
                    money = re.search(r'([+-]?([0-9]*[.])?[0-9]+%)',new[index_money:]).group(1)
                list_.append({"Time":day,"Stock":scale,"Money":money})
            except:
                continue
        temp = pd.DataFrame.from_records(list_)
        if news.empty:
          return 0
        temp.to_csv({self.path_object["F1"]["Dividend"]}+symbol+".csv")
        return temp
      except:
        return -1
    pass