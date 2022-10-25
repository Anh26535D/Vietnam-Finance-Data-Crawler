import pandas as pd
import numpy as np
class Volume():
    def __init__(self,dict_path_) -> None:
        self.path_object = dict_path_
        pass

    def find_volume_withtile(self,data,title):
        t = list(data['Title']).index(title)
        value = list(data['Value'])[t]
        return value

class VolumeCafeF(Volume):
    def __init__(self, dict_path_) -> None:
        super().__init__(dict_path_)

    def getVolumeNow(self,symbol):
        try:
            data = pd.read_csv(f'{self.path_object["F0"]["VolumeNow"]}/{symbol}.csv')
            volume_luuhanh = self.find_volume_withtile(data,"KLCP đang lưu hành:")
            return float(volume_luuhanh)
        except:
            return np.nan

class VolumeVietStock(Volume):
    def __init__(self, dict_path_) -> None:
        super().__init__(dict_path_)
    def rename(self,data):
        data.columns = ["Title",'Value']
        return data
    def getVolumeNow(self,symbol):
        try:
            data = pd.read_csv(f'{self.path_object["F0"]["VolumeNow"]}/{symbol}.csv')
            data = self.rename(data)
            volume_luuhanh = self.find_volume_withtile(data,"KL Cổ phiếu đang lưu hành")
            return float(volume_luuhanh.replace(",",""))
        except:
            return np.nan