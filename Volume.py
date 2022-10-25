import pandas as pd
from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

def getVolume(symbol):
    return symbol
F_START = FU.GetDateUpdateEndStart()
F_END = FU.GetDateUpdateEnd()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>F_START and date <= F_END:
        F_RANGE.append(date)

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    try:
        getVolume(symbol)
    except:
        pass
