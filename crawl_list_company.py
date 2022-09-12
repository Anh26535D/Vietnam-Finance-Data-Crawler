import pandas as pd
from Crawl import VietStock
import Flow.PATH_env as PATH_env


PATH_ = PATH_env.PATH_ENV()
t = VietStock.Other("T")
t.login_VS()
data = t.Listing()

data.to_csv(f'{PATH_.joinPath(PATH_.PATH_MAIN_CURRENT,"List_company",PATH_.DayCurrent)}.csv',index=False)