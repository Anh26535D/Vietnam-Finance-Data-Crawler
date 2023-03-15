import pandas as pd
import sys

sys.path.append(r'C:\DataVietNam')
sys.path.append(r'C:\DataVietNam\TransformData\VietNam')
from base.PATH_UPDATE import *
from VAR_GLOBAL_CONFIG import *
from base.Setup import *
from Flow.ulis import *

CURRENT = 0
PRICE = pd.DataFrame()
for symbol in SYMBOL:
    CURRENT+=1 
    try:
        df = pd.read_csv(FU.joinPath(FU.PATH_CLOSE,f"{symbol}.csv"))
        df["Symbol"] = [symbol for i in df.index]
    except:
        print(symbol)
        continue
    PRICE = pd.concat([PRICE,df], ignore_index=True)
    progress_bar(CURRENT,TOTAL,text="Gom Giá")

PRICE.to_json(f"{FU.PATH_MAIN_CURRENT}/PRICE_HSX.json",index="orient")