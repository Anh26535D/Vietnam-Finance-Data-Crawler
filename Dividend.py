import pandas as pd
from Flow import Folder
import re
import TransformData.VietNam.PATH_UPDATE as PATH_UPDATE

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

dict_path = PATH_UPDATE.dict_path


List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
field = ""
for symbol in List_Symbol["Mã CK▲"]:
    try:
        Dividend(symbol,field)
    except:
        pass