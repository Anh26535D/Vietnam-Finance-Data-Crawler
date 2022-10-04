import pandas as pd

class Volume():
    def __init__(self,dict_path_) -> None:
        self.path_object = dict_path_
        pass

    def find_volume_withtile(self,data,title):
        t = list(data['Title']).index(title)
        value = list(data['Value'])[t]
        return value
    
    def getVolumeNow(self,symbol):
        data = pd.read_csv(f'{self.path_object["F0"]["VolumeNow"]}/{symbol}.csv')
        volume_niemyet = self.find_volume_withtile(data,"KLCP đang niêm yết:")
        volume_luuhanh = self.find_volume_withtile(data,"KLCP đang lưu hành:")
        return volume_niemyet,volume_luuhanh
