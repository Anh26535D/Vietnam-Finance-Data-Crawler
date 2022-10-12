import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')

from base import Compare
from base.Financial import CafeF,VietStock
from base.PATH_UPDATE import *

# CafeF
List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"][:5]:
    CF = CafeF(dict_path_cf)
    CF.run(symbol,"Year")
    CF.run(symbol,"Quarter")

    VS = VietStock(dict_path_vs)
    VS.run(symbol,"Year")
    VS.run(symbol,"Quarter")

def setup_Feature(type_time):
    if type_time == "Year":
        sheet_name = "Total"
    else:
        sheet_name = "Quarter"
    data_field = pd.read_excel(f'{dict_path_vs["Feature"]}/Feature_Standard_Library.xlsx',sheet_name=sheet_name)
    data_field = data_field.rename(columns={"column":"Feature"})
    return data_field

def RunCompare(type_time):
    data_field = setup_Feature(type_time)
    for symbol in List_Symbol["Mã CK▲"][:5]:
        try:
            C = Compare.CompareFinancial(symbol,PATH_FT,type_time,data_field)
            C.get_field("CF","VS").to_csv(FU.joinPath(FU.PATH_COMPARE,"Financial",type_time,f"{symbol}.csv"),index=False)
        except:
            print("Loi",symbol)
RunCompare("Year")
RunCompare("Quarter")