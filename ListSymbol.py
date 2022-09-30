import pandas as pd
from datetime import datetime
from Flow.Folder import FolderCrawl, FolderData, FolderUpdate
from Flow.PATH_env import PATH_ENV
import os

FC = FolderCrawl()
FU = FolderUpdate()

def GetListSymbol():
    Folder = FC.GetDateUpdate()
    PATH_FROM = FC.joinPath(FC.PATH_MAIN,Folder,"List_company.csv")
    PATH_TO = FU.joinPath(FU.PATH_MAIN,Folder,"List_company.csv")
    pd.read_csv(PATH_FROM).to_csv(PATH_TO,index=False)

GetListSymbol()