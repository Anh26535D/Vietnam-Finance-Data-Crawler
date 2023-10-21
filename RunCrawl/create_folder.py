import sys
# sys.path.append(r'C:\DataVietNam')
sys.path.append(r'E:\vis\vis_vietnamese_data\Vis_Data_VietNam')
from Flow import Folder
try:
    create = Folder.FolderCrawl()
    create.Run_Create_Folder()
except:
    pass
