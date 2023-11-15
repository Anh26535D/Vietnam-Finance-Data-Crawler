import sys
# sys.path.append(r'C:\DataVietNam')
sys.path.append(r'E:\vis\vis_vietnamese_data\Vis_Data_VietNam')
from Flow import Folder
try:
    folder_creator = Folder.FolderCrawl()
    folder_creator.run()
except:
    pass
