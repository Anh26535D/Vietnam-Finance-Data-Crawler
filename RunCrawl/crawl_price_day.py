import sys
sys.path.append(r'C:\DataVietNam')
from Crawl import SSI
from Flow import PATH_env

PATH_ = PATH_env.PATH_ENV("Ingestion")

t = SSI.Price()
t.getPriceToDayAllExchange().to_csv(f"{PATH_.REAl_DAY_CLOSE}/2023-03-13.csv",index=False)