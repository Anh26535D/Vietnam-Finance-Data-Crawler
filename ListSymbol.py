import pandas as pd
from datetime import datetime
from Flow.PATH_env import PATH_ENV
import os
PATH_ = PATH_ENV("Ingestion")

def GetDateUpdate():
    list_date = os.listdir(PATH_.PATH_MAIN)
    arr = []
    for day in list_date:
        if len(day) == 10:
            arr.append(day)
    arr.sort()
    return arr[-1]

def GetListSymbol():
    PATH_ = PATH_ENV("Ingestion")
    Folder = GetDateUpdate()
    PATH_FROM = PATH_.joinPath(PATH_.PATH_MAIN,Folder,"List_company.csv")
    PATH_ = PATH_ENV("Raw_VIS")
    PATH_FROM = PATH_.joinPath(PATH_.PATH_MAIN,Folder,"List_company.csv")
    pd.read_csv(PATH_FROM).to_csv(PATH_FROM,index=False)
GetListSymbol()