import sys
sys.path.append(r'C:\DataVietNam')
import pandas as pd
from Crawl import VietStock
import Flow.PATH_env as PATH_env
import time
def run_reset_vs():
    # global webVS
    # try:
    #     webVS = VietStock.Other("")
    #     webVS.login_VS()
    # except:
    print("Tam Nghi VS-------------------")
    webVS.turn_off_drive()
    time.sleep(100)
    # run_reset_vs()


PATH_ = PATH_env.PATH_ENV("Ingestion")
check = False
while check == False:
    try:
        List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
        check = True
    except:
        try:
            webVS = VietStock.Other()
            webVS.login_VS()
            data = webVS.Listing()
            data.to_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv',index=False)
            webVS.turn_off_drive()
            check = True
        except:
            run_reset_vs()