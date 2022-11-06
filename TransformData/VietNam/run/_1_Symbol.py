import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')

from datetime import datetime
from Flow.Folder import FolderCrawl, FolderData, FolderUpdate
from Flow.PATH_env import PATH_ENV
from VAR_GLOBAL_CONFIG import *

FC = FolderCrawl()
FU = FolderUpdate()

def GetListSymbol(FROM,TO):
    PATH_FROM = FC.joinPath(FC.PATH_MAIN,FROM,"List_company.csv")
    PATH_TO = FU.joinPath(FU.PATH_MAIN,TO,"List_company.csv")
    pd.read_csv(PATH_FROM).to_csv(PATH_TO,index=False)
FROM = FC.GetDateUpdate(END_DAY_UPDATE)
TO = FU.GetDateUpdate(END_DAY_UPDATE)
GetListSymbol(FROM,TO)