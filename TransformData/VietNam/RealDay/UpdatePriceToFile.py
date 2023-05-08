import datetime
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
import pandas as pd
from Flow import Folder
def fillter(df,value=500000000):
    df["Value"] = df['Price']*df['Volume']
    return df[df["Value"]>=value]

ComDelete = ["TCH","OGC","KPF"]

today = datetime.datetime.today()

# today = datetime.datetime(2023,3,31)
# today = datetime.datetime(2023,3,22)
FC = Folder.FolderCrawl()
F_WH = Folder.FolderWH()

LinkSymbol = f'{FC.joinPath(FC.REAl_DAY,"List_company")}.csv'
LinkFileGetPrice = f"{FC.REAl_DAY_CLOSE}/{today.strftime('%Y-%m-%d')}.csv"
LinkFilePriceAppend = f"{F_WH.PATH_CLOSE}/PriceClose_HOSE.csv"

Link_Symbol = pd.read_csv(LinkSymbol).rename(columns={"Mã CK▲":'Symbol'})
PriceGet = pd.read_csv(LinkFileGetPrice)
PriceGet = fillter(PriceGet)
PriceTotal = pd.read_csv(LinkFilePriceAppend)

Link_Symbol["CheckComDelete"] = Link_Symbol["Symbol"].apply( lambda row: row in ComDelete)

Link_Symbol = Link_Symbol[Link_Symbol["CheckComDelete"] == False]
MergePrice = pd.merge(Link_Symbol,PriceGet,how="left",on="Symbol")

PriceGet = MergePrice[MergePrice["Exchange"] =="HOSE"][['Symbol','Price']]

MergePrice = pd.merge(PriceTotal,PriceGet,how="outer",left_on="SYMBOL",right_on="Symbol")
try:
    MergePrice = MergePrice.drop(columns = [today.strftime('%Y-%m-%d')])
except:
    pass
MergePrice[today.strftime('%Y-%m-%d')] = MergePrice["Price"]/1000.0
MergePrice = MergePrice.drop(columns = ["Symbol","Price"])
MergePrice = MergePrice.fillna(-1)
# print(MergePrice[["Symbol",today.strftime('%Y-%m-%d'),'2023-03-14']])
MergePrice.to_csv(LinkFilePriceAppend,index=False)





