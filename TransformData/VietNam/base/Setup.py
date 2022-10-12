import sys
sys.path.append(r'C:\DataVietNam')
from Flow import Folder


FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()

F_START = FU.GetDateUpdateNearest()
F_END = FU.GetDateUpdate()
F_BASE = FC.getListPath()
F_RANGE = []
for date in F_BASE:
    if date>=F_START and date <= F_END:
        F_RANGE.append(date)

print(F_START,F_END,F_RANGE)