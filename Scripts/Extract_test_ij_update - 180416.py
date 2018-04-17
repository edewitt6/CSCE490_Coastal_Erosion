# Created by Euan-Angus MacLeod
#
#Description: This code attempts to extract the lat, lon and the corresponding indices that store the environmental data
#input: tos_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc
#output: SST_SP.csv
######################################

import netCDF4 
import numpy as np
import math
import csv
import os
import arcpy

from arcpy import env
path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project"
env.workspace = path
env.scratchWorkspace = path
env.overwriteOutput = True

from netCDF4 import Dataset

#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932


tol = 1 #search tolerance (decimal degree)

closest_dist = 10000000000000000000000
closest_i = 1000
closest_j = 1000


main_dir = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Data\\SST\\Historical\\CNRM_hist\\CNRM_hist"


# for folder_name in os.listdir(main_dir):
#     #print folder_name
#     folder_path = main_dir + '\\' + folder_name
    
    #start NetCDF data extraction
for file_name in os.listdir(main_dir):

    print'---------------------------------------------'

    file = main_dir + '\\' + file_name #add if the loop above is used:  '\\' + folder_name +

    nc = Dataset(file,'r')
    
    tos = nc.variables['tos']
    lat = nc.variables['lat']
    lon = nc.variables['lon']
    time = nc.variables['time']
    
    print tos
    print lat
    print lon
    print time
    
    
    print 'Calculating closest model point to Drew Point in', file_name, '\n'
    for i in range(lat.shape[0]):
        for j in range(lon.shape[1]):
            if lat[i][j] > (DP_lat - tol) and lat[i][j] < (DP_lat + tol):
                if lon[i][j] > (DP_lon - tol) and lon[i][j] < (DP_lon + tol):
                    dist_DP = math.sqrt((DP_lon - lon[i][j])**2 + (DP_lat - lat[i][j])**2) 
                    
                    if dist_DP < closest_dist:
                        closest_dist = dist_DP
                        closest_i = i
                        closest_j = j
                    
    print 'Closest model point to Drew Point:'
    print 'Lat:', lat[closest_i][closest_j], 'Lon:', lon[closest_i][closest_j], 'i:', closest_i, 'j:', closest_j
    
    
    # Extract data from model for the appropriate time series - Arcpy
    coords = "i " + str(closest_i) + ";j " + str(closest_j)
    
    out_csv_file =  output_dir + "\\" +  site + "_" + file_name + ".xls"
    
    
    
    # Process: Make NetCDF Table View
    arcpy.MakeNetCDFTableView_md(file, "tos", "raw_table", "time", coords, "BY_VALUE")
    
    print 'Extracted data written to', out_csv_file, '\n'
    # Process: Table To CSV
    arcpy.TableToExcel_conversion("raw_table", out_csv_file, "ALIAS", "CODE")   
 

