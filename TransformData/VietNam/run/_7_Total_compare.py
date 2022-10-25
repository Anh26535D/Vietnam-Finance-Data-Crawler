import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')


from base.PATH_UPDATE import *
from base.Setup import *


dict_compare = {
    "Financial_Quarter": pd.DataFrame(),
    # "Financial_Year": pd.DataFrame(),
    # "Dividend": pd.DataFrame()
}

def GetError(symbol,field):
    path = field.replace("_","/")
    df_current = pd.read_csv(f"{PATH_COMPARE}/{path}/{symbol}.csv")
    df_current["Symbol"] = [symbol for i in df_current.index]
    df_error = df_current[df_current["Compare"]==2].reset_index(drop = True)
    # df_error = df_current.reset_index(drop = True)
    dict_compare[field] = pd.concat([dict_compare[field],df_error],ignore_index=True)
    return df_error

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for key in dict_compare.keys():
    for symbol in List_Symbol["Mã CK▲"]:
        try:
            GetError(symbol,key)
        except:
            continue
    dict_compare[key].to_excel(f"{PATH_COMPARE}/{key}_2.xlsx",index=False)
