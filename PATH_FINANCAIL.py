from Flow import Folder

FC = Folder.FolderCrawl()
FU = Folder.FolderUpdate()
F_END = FU.GetDateUpdate()

PATH_F0_TOTAL = FC.joinPath(FC.PATH_MAIN,F_END,F)
PATH_F0 = "/content/drive/MyDrive/DataVIS/VietNam/Data Lake/Ingestion/Day 0/CafeF/Financial/"
PATH_F1 = "/content/drive/MyDrive/DataVIS/VietNam/Data Lake/Raw_VIS/Day 0 /CafeF/Financial/Financial_F1/"
PATH_F2 = "/content/drive/MyDrive/DataVIS/VietNam/Data Lake/Raw_VIS/Day 0 /CafeF/Financial/Financial_F2/"
PATH_F3 = "/content/drive/MyDrive/DataVIS/VietNam/Data Lake/Raw_VIS/Day 0 /CafeF/Financial/Financial_F3/"
LINK_QUATER = "Quarter/"
LINK_YEAR = "Year/"
BALANCE = "BalanceSheet/"
INCOME = "IncomeStatement/"
DIRECT = "CashFlowDirect/"
INDIRECT = "CashFlowInDirect/"
PRICE = "Price/"
VOLUME_ADDITIONAL = "Volume/VolumeAdditionailEvents/"
VOLUME_TREASURY_SHARE = "Volume/TreasuryShares/"
DIVIDEND = "Dividend/"
VOLUME_NOW="Volume/VolumeNow/"
dict_path = { "F0":{"Balance_Year": PATH_F0 + LINK_YEAR + BALANCE,
                    "Income_Year": PATH_F0 + LINK_YEAR + INCOME,
                    "Direct_Year": PATH_F0 + LINK_YEAR + DIRECT,
                    "InDirect_Year": PATH_F0 + LINK_YEAR + INDIRECT,
                    "Balance_Quater": PATH_F0 + LINK_QUATER + BALANCE,
                    "Income_Quater": PATH_F0 + LINK_QUATER + INCOME,
                    "Direct_Quater": PATH_F0 + LINK_QUATER + DIRECT,
                    "InDirect_Quater": PATH_F0 + LINK_QUATER + INDIRECT,
                    'Price':PATH_F0_TOTAL + PRICE,
                    'VolumeAdditionalEvents':PATH_F0_TOTAL + VOLUME_ADDITIONAL,
                    'Dividend':PATH_F0_TOTAL + DIVIDEND,
                    'TreasuryShares':PATH_F0_TOTAL + VOLUME_TREASURY_SHARE,
                    'VolumeNow':PATH_F0_TOTAL + VOLUME_NOW,
                    },
                "F1":{"Balance_Year": PATH_F1 + LINK_YEAR + BALANCE,
                    "Income_Year": PATH_F1 + LINK_YEAR + INCOME,
                    "Direct_Year": PATH_F1 + LINK_YEAR + DIRECT,
                    "InDirect_Year": PATH_F1 + LINK_YEAR + INDIRECT,
                    "Balance_Quater": PATH_F1 + LINK_QUATER + BALANCE,
                    "Income_Quater": PATH_F1 + LINK_QUATER + INCOME,
                    "Direct_Quater": PATH_F1 + LINK_QUATER + DIRECT,
                    "InDirect_Quater": PATH_F1 + LINK_QUATER + INDIRECT,
                    },
                "F2":{"Balance_Year": PATH_F2 + LINK_YEAR + BALANCE,
                    "Income_Year": PATH_F2 + LINK_YEAR + INCOME,
                    "Direct_Year": PATH_F2 + LINK_YEAR + DIRECT,
                    "InDirect_Year": PATH_F2 + LINK_YEAR + INDIRECT,
                    "Balance_Quater": PATH_F2 + LINK_QUATER + BALANCE,
                    "Income_Quater": PATH_F2 + LINK_QUATER + INCOME,
                    "Direct_Quater": PATH_F2 + LINK_QUATER + DIRECT,
                    "InDirect_Quater": PATH_F2 + LINK_QUATER + INDIRECT,
                    },
                "F3":{"Balance_Year": PATH_F3 + LINK_YEAR + BALANCE,
                    "Income_Year": PATH_F3 + LINK_YEAR + INCOME,
                    "Direct_Year": PATH_F3 + LINK_YEAR + DIRECT,
                    "InDirect_Year": PATH_F3 + LINK_YEAR + INDIRECT,
                    "Balance_Quater": PATH_F3 + LINK_QUATER + BALANCE,
                    "Income_Quater": PATH_F3 + LINK_QUATER + INCOME,
                    "Direct_Quater": PATH_F3 + LINK_QUATER + DIRECT,
                    "InDirect_Quater": PATH_F3 + LINK_QUATER + INDIRECT,
                    },
             }