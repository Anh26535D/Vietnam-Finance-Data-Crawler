import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL import *
from base.Financial import CafeF,VietStock
from base.Setup import *
from Flow.ulis import *

Data = pd.read_excel(f"{PATH_COMPARE}/{QUARTER_FINANCAIL_FIX_FILE}.xlsx")
DataFix = pd.read_excel(f"{PATH_COMPARE}/{QUARTER_FINANCAIL_FIX_FILE_BY_HUMAN}.xlsx",sheet_name="Data-Fixed")
DataDelete = pd.read_excel(f"{PATH_COMPARE}/{QUARTER_FINANCAIL_FIX_FILE_BY_HUMAN}.xlsx",sheet_name="Com_delete")
Symbol_delete = DataDelete["Symbol"]
total = len(SYMBOL)
current = 0
def read_file(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame()

def alalyst_code(code):
    source = None
    code = int(code)
    if code == 1:
        source = "CafeF"
    elif code == 2 or code ==0:
        source = "FileFix"
    else:
        pass
    return source

def getDataFixError(x,y,source):
    if source == "CafeF":
        return x
    elif source == "FileFix":
        return y
    return None

Data["Source"] = Data["Compare"].apply(lambda row: alalyst_code(row))
DataFix = DataFix[["Feature","Symbol","FIx_Trang"]]
Data_Source = pd.merge(Data,DataFix,how="outer",on=["Feature","Symbol"])
Data_Source[QUARTER_KEY] = Data_Source.apply(lambda row: getDataFixError(row[f"{QUARTER_KEY}_x"],row["FIx_Trang"],row["Source"]),axis=1)
Data_Source = Data_Source[["Feature","Symbol",QUARTER_KEY]]

DATA = pd.DataFrame()
for com in SYMBOL:
    current+=1
    if not com in Symbol_delete:
        df = Data_Source[Data_Source["Symbol"] == com]
        df = df[["Feature",QUARTER_KEY]].reset_index(drop=True).T
        df = df.rename(columns=df.iloc[0])
        df = df.drop(df.index[0])
        df["Symbol"] = [com for i in df.index]
        DATA = pd.concat([DATA,df],ignore_index=True)
    progress_bar(current,total,text="Bien doi hang")
DATA.to_excel(f"{FU.PATH_MAIN_CURRENT}/FINANCAIL_{QUARTER_KEY.replace('/','_')}.xlsx",index=False)
