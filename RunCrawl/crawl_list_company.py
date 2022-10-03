import pandas as pd
from ..Crawl import VietStock
import Flow.PATH_env as PATH_env


PATH_ = PATH_env.PATH_ENV()
try:
    List_Symbol = pd.read_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv')
except:
    t = VietStock.Other("T")
    t.login_VS()
    data = t.Listing()
    data.to_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company")}.csv',index=False)