from Flow import Folder

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()
F_NEED_RUN = FC.GetDateUpdate()

PATH_FI = FC.joinPath(FC.PATH_MAIN, F_NEED_RUN)
PATH_FT = FU.joinPath(FU.PATH_MAIN,F_NEED_RUN)
LINK_QUATER = "Quarter"
LINK_YEAR = "Year"
BALANCE = "BalanceSheet"
INCOME = "IncomeStatement"
PRICE = "Close"
VOLUME_ADDITIONAL = "Volume/VolumeAdditionailEvents"
VOLUME_TREASURY_SHARE = "Volume/TreasuryShares"
DIVIDEND = "Dividend"
VOLUME="Volume"
VOLUME_NOW = "VolumeNow"
dict_path_cf = { "F0":{"Balance_Year": FC.joinPath(PATH_FI,"CafeF/Financial",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FI,"CafeF/Financial",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FI,"CafeF/Financial",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FI,"CafeF/Financial",LINK_QUATER,BALANCE),
                    'Price': FC.joinPath(PATH_FI,PRICE,"CafeF"),
                    'Dividend': FC.joinPath(PATH_FI,DIVIDEND,"CafeF"),
                    'VolumeNow':FC.joinPath(PATH_FI,VOLUME,"CafeF",),
                    },
                "F1":{
                    "Balance_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F1",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F1",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F1",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F1",LINK_QUATER,INCOME),
                    },
                "F2":{
                    "Balance_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F2",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F2",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F2",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F2",LINK_QUATER,INCOME),
                    },
                "F3":{
                    "Balance_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F3",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F3",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F3",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"CafeF/Financial/Financial_F3",LINK_QUATER,INCOME),
                    },
             }

dict_path_vs = { "F0":{"Balance_Year": FC.joinPath(PATH_FI,"VietStock/Financial",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FI,"VietStock/Financial",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FI,"VietStock/Financial",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FI,"VietStock/Financial",LINK_QUATER,BALANCE),
                    'Price': FC.joinPath(PATH_FI,PRICE,"VietStock"),
                    'Dividend': FC.joinPath(PATH_FI,DIVIDEND,"VietStock"),
                    'VolumeNow':FC.joinPath(PATH_FI,VOLUME,"VietStock",),
                    },
                "F1":{
                    "Balance_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F1",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F1",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F1",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F1",LINK_QUATER,INCOME),
                    },
                "F2":{
                    "Balance_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F2",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F2",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F2",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F2",LINK_QUATER,INCOME),
                    },
                "F3":{
                    "Balance_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F3",LINK_YEAR,BALANCE),
                    "Income_Year": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F3",LINK_YEAR,INCOME),
                    "Balance_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F3",LINK_QUATER,BALANCE),
                    "Income_Quater": FC.joinPath(PATH_FT,"VietStock/Financial/Financial_F3",LINK_QUATER,INCOME),
                    },
             }