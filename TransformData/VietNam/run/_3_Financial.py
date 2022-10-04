import pandas as pd
import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam\base')

from base.Financial import CafeF,VietStock,Compare
from base.PATH_UPDATE import *

# CafeF
List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
CF = CafeF(dict_path_cf)
CF.Financial_F0_to_F1("AAA","Balance_Year")




