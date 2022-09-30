import pandas as pd
from Flow import Folder
import re
import PATH_FINANCAIL

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

dict_path = PATH_FINANCAIL.dict_path
def Dividend(symbol,field):
      list_ = []
      try:
        news = pd.read_csv(dict_path[field][0]+symbol+".csv")
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
        temp.to_csv(dict_path[LAYER][field][1]+symbol+".csv")
        return temp
      except:
        return -1

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
field = ""
for symbol in List_Symbol["Mã CK▲"]:
    try:
        Dividend(symbol,field)
    except:
        pass