import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL import *
from base.Financial import CafeF,VietStock
from base.Setup import *
from Flow.ulis import *

CURRENT = 0
Data = pd.read_excel(f"{PATH_COMPARE}/Dividend.xlsx")
Data = Data[["Time","Fix_Trang","Symbol"]]
Data["Money"] = Data["Fix_Trang"].apply(lambda row:row.split("_")[0])
Data["Stock"] = Data["Fix_Trang"].apply(lambda row:row.split("_")[-1])
Data[["Time","Money","Stock","Symbol"]].to_excel(f"{FU.PATH_MAIN_CURRENT}/DIVIDEND.xlsx",index=False)
