# Author: Eric DeWitt
# Purpose: Convert Excel files to a more readable CSV format

import csv
import os
import pandas as pd

# Input your own directory for the Excel files you want to convert
os.chdir("C:\Your Directory")

names = []
names2 = []

# Goes through listed directory and makes lists of all the xls,xlsx files
for items in os.listdir(os.getcwd()):
    if items.endswith(".xlsx"):
        names.append(items)
        names2.append(items.replace("xlsx","csv"))
    elif items.endswith(".xls"):
        names.append(items)
        names2.append(items.replace("xls","csv"))

# Creates CSV files using the pandas module
for i in range(0,names.__len__()):
    data_xls = pd.read_excel(names[i],index_col=0)
    data_xls.to_csv(names2[i], encoding='utf-8')
