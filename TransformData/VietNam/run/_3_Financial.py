import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')

from base import Compare
from base.Financial import CafeF,VietStock
from base.PATH_UPDATE import *
from base.Setup import *
Type_Time = "Quarter"
# CafeF
df_check_list = pd.DataFrame()
def transform(symbol,field):
    global df_check_list
    CF = CafeF(dict_path_cf)
    cf = CF.run(symbol,field)
    VS = VietStock(dict_path_vs)
    vs = VS.run(symbol,field)
    df = pd.DataFrame({"Symbol": [symbol],
                        "Type_Time": [field],
                        "CafeF": [cf],
                        "VietStock":[vs]})
    df_check_list = pd.concat([df_check_list,df],ignore_index=True)

List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')

for symbol in SYMBOL:
    transform(symbol,"Quarter")

df_check_list.to_excel(FU.joinPath(FU.PATH_COMPARE,f"Financial_{Type_Time}_CheckList.xlsx"))

def setup_Feature(type_time):
    if type_time == "Year":
        sheet_name = "Total"
    else:
        sheet_name = "Quarter"
    data_field = pd.read_excel(f'{dict_path_vs["Feature"]}/Feature_Standard_Library.xlsx',sheet_name=sheet_name)
    data_field = data_field.rename(columns={"column":"Feature"})
    return data_field

def RunCompare(type_time):
    can_t_compare = []
    data_field = setup_Feature(type_time)
    for symbol in SYMBOL:
        try:
            C = Compare.CompareFinancial(symbol,PATH_FT,type_time,data_field)
            C.get_field("CF","VS").to_csv(FU.joinPath(FU.PATH_COMPARE,"Financial",type_time,f"{symbol}.csv"),index=False)
        except:
            can_t_compare.append(symbol)
    pd.DataFrame({"Error_Compare":symbol}).to_excel(FU.joinPath(FU.PATH_COMPARE,"Error",f"{type_time}.xlsx"),index=False)        



RunCompare("Quarter")