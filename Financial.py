LAYER = "F0"
import re
list_result = []
def getCheckListFinancail(field):
  list_result = []
  for symbol in list_symbol:
    try:
      with open(f'{dict_path[LAYER][field]}{symbol}.json', "r",encoding='utf8') as j:
        data = json.loads(j.read())
      list_year = []
      for year in range(2000,2022):
        try:
          data_year = pd.DataFrame.from_records(data[f'[{year}]'])
          if data_year[f'[{year}]'].isnull().all():
            list_year.append(0)
          else:
            list_year.append(1)
        except:
          list_year.append(np.nan)
    except:
      list_year = [np.nan for i in range(2000,2022)]
    list_result.append(list_year)
  return pd.DataFrame(list_result, columns = [i for i in range(2000,2022)],index=list_symbol)
def getCheckListFinancailQ(field):
    result = pd.DataFrame()
    for symbol in list_symbol:
        com = pd.DataFrame({"symbol":[symbol]})
        try:
            with open(f'{dict_path[LAYER][field]}{symbol}.json', "r",encoding='utf8') as j:
                data = json.loads(j.read())
            for key in list(data.keys()):
                match = re.findall('([0-9]-[0-9]+)', key)
                time = match[0]
                try:
                    data_year = pd.DataFrame.from_records(data[key])
                    if data_year[key].isnull().all():
                        com[time] = [0]
                    else:
                        com[time] = [1]
                except:
                    com[time] = [np.nan]
        except:
              pass
        result = pd.concat([result,com],ignore_index=True)
    return result
  
def getCheckListClose(field):
  list_result = []
  for symbol in list_symbol:
    try:
      data = pd.read_csv(f'{dict_path[LAYER][field]}{symbol}.csv')
      if data[data.columns[0]].isnull().all():
        list_result.append(0)
      else:
        list_result.append(1)
    except:
      list_result.append(np.nan)
  return pd.DataFrame(list_result,index=list_symbol)

def getCheckList(field):
  list_result = []
  for symbol in list_symbol:
    try:
        data = pd.read_csv(f'{dict_path[LAYER][field]}{symbol}.csv')
        if data[data.columns[0]].isnull().all():
            list_result.append(0)
        else:
            list_result.append(1)
    except:
      list_result.append(np.nan)
  return pd.DataFrame(list_result,index=list_symbol)

def getCheckListUpDown(field):
  list_result = []
  for symbol in list_symbol:
    try:
      data = pd.read_csv(f'{dict_path[LAYER][field]}{symbol}.csv')
      if data[data.columns[0]].isnull().all():
        list_result.append(0)
      else:
        list_result.append(1)
    except:
      list_result.append(np.nan)
  return pd.DataFrame(list_result,index=list_symbol)