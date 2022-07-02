import numpy as np
import pandas as pd
from Crawl import TVSI

com = TVSI.Financail(symbol="AAA")
result = pd.DataFrame({"field":[]})
list_field = []
for year in range(2000,2023):
    try:
      df1 = com.get_Income(year=year)
      for col in df1.columns:
        if col in result.columns:
          list_field.append(col)
      result = pd.merge(df1,result,on=list_field,how='outer')
    except:
      continue
result.to_csv("AAA.csv",index=False)