import sys
sys.path.append(r'E:\vis\vis_vietnamese_data\DataVietNam')

import datetime
from Flow import PATH_env
from Crawl import SSI

PATH_ = PATH_env.PATH_ENV("Ingestion")

t = SSI.Price()
day = datetime.datetime.today()


iboard_data = t.getIBoardAllExchange()
iboard_data.to_csv(
    f"{PATH_.REAl_DAY_IBOARD}/{day.strftime('%Y-%m-%d')}.csv", index=False)


trading = iboard_data[["stockSymbol", "matchedPrice", "nmTotalTradedQty", "refPrice","exchange"]].rename(
    columns={"stockSymbol": "Symbol", 
             "matchedPrice": "Price", 
             "nmTotalTradedQty": "Volume", 
             "refPrice": "prePrice",
             'exchange':"Exchange"})
trading["Day"] = [day.strftime('%Y-%m-%d') for i in trading.index]
trading.to_csv(
    f"{PATH_.REAl_DAY_CLOSE}/{day.strftime('%Y-%m-%d')}.csv", index=False)
