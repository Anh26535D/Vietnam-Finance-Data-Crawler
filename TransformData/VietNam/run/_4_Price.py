import sys
sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')

from Flow import Folder
import math
from Flow.PATH_env import PATH_ENV
from Flow.ulis import *
from base.Price import *
from base.Setup import *


TP = TransformPrice(FU,FC,F_RANGE)
List_Symbol = pd.read_csv(f'{FU.joinPath(FU.PATH_MAIN_CURRENT,"List_company")}.csv')
for symbol in List_Symbol["Mã CK▲"]:
    try:
        TP.concat_source(symbol).to_csv(FU.joinPath(FU.PATH_CLOSE,f"{symbol}.csv"),index=False)
    except:
        print(symbol)