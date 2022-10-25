import sys
import pandas as pd
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from datetime import datetime
from Flow.Folder import FolderCrawl, FolderData, FolderUpdate
from base.PATH_UPDATE import *

link = f"{PATH_COMPARE}/Financial_Quarter.xlsx"
data = pd.read_excel(link)
data_feature = pd.read_excel(f'{FR.PATH_MAIN}/Feature_Standard_Library.xlsx',sheet_name="VietStock")
data = pd.merge(data,data_feature,how="left",left_on="Feature",right_on="VIS_Raw_F2")
data1 = data[['Feature','2/2022_x','2/2022_y','Compare','Symbol',"Ingestion"]]
data1.to_excel(link,index=False)