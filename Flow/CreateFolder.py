from calendar import c
from datetime import datetime
import os
from Flow import PATH_env


class FolderData(PATH_env.PATH_ENV):
    def __init__(self):
        super().__init__()
        

    def createFolder(self,path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

    def folderClose(self):
        path = self.PATH_CLOSE
        self.createFolder(path)
        for obj in self.CloseObject:
            self.createFolder(self.joinPath(path,obj))
    
    def folderDividend(self):
        path = self.PATH_DIVIDEND
        self.createFolder(path)
        for obj in self.DividendObject:
            if obj == "VietStock":
                for p_obj in self.DividendPartObject:
                    self.createFolder(self.joinPath(path,obj))
                    self.createFolder(self.joinPath(path,obj,p_obj))
            else:
                self.createFolder(self.joinPath(path,obj))
    
    def folderFinancial(self):
        path = self.PATH_FINANCIAL
        self.createFolder(path)
        for obj in self.FinancialObject:
            for t_time in self.Type_Time:
                for p_obj in self.FinancialPartObject:
                    self.createFolder(self.joinPath(path,obj))
                    self.createFolder(self.joinPath(path,obj,t_time))
                    self.createFolder(self.joinPath(path,obj,t_time,p_obj))

    def folderVolume(self):
        path = self.PATH_VOLUME
        for obj in self.VolumeObject:
            for p_obj in self.VolumePartObject:
                self.createFolder(self.joinPath(path,obj))
                self.createFolder(self.joinPath(path,obj,p_obj))
                

    def Run_Create_Folder(self):
        self.folderClose()
        self.folderDividend()
        self.folderFinancial()
        self.folderVolume()