from datetime import datetime
import os
from Flow import PATH_env



class FolderData(PATH_env.PATH_ENV):
    def __init__(self):
        super().__init__()
        self.CloseObject = ["CafeF","StockBiz"]
        self.FinancialObject = ["CafeF","VietStock"]
    
    def createFolder(self,path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

    def folderClose(self):
        path = self.PATH_CLOSE
        self.createFolder(path)
        for obj in self.CloseObject:
            self.createFolder(self.joinPath(path,obj))
    
    def folderFinancial(self):
        path = self.PATH_FINANCIAL
        self.createFolder(path)
        for obj in self.FinancialObject:
            self.createFolder(self.joinPath(path,obj))
    
    def Run_Create_Folder(self):
        self.folderClose()

        

    