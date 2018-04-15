# Author: Eric DeWitt
# Date: 15 April 2018
# Purpose: Module to convert excel files to csv format

import csv
import os
import pandas as pd

def convert(cur_dir):
    os.chdir(cur_dir)
    
    xcel_files = []
    csv_files = []
    
    # Goes through listed directory and makes lists of all the xls,xlsx files
    for items in os.listdir(os.getcwd()):
        if items.endswith(".xlsx"):
            xcel_files.append(items)
            csv_files.append(items.replace("xlsx","csv"))
        elif items.endswith(".xls"):
            xcel_files.append(items)
            csv_files.append(items.replace("xls","csv"))
    
    # Creates CSV files using the pandas module
    for i in range(0,xcel_files.__len__()):
        mfile = pd.ExcelFile(xcel_files[i])
        for sheet in mfile.sheet_names:
            data = pd.read_excel(mfile,sheetname=sheet,index_col=0)
            data.to_csv(csv_files[i], mode='a', encoding='utf-8')