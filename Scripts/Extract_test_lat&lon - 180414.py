# Created by Euan-Angus MacLeod
#
#Description: This code attempts to extract the lat, lon and the corresponding indices that store the environmental data
#input: uas_3hr_GFDL-CM3_historical_r1i1p1_1975010100-1979123123.nc
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

os.chdir("C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Scripts")

file = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Data\\Wind\\GFDL_NC\\Historic\\Ua\\uas_3hr_GFDL-CM3_historical_r1i1p1_1975010100-1979123123.nc"

nc = Dataset(file,'r')

uas = nc.variables['uas']
lat = nc.variables['lat']
lon = nc.variables['lon']
time = nc.variables['time']

print uas
print lat
print lon
print time

## Find Model Data Location

#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932

model_lat = lat[:]
model_lon = lon[:]

tol = 1 #search tolerance (decimal degree)

closest_dist = 10000000000000000000000
closest_i = 1000
closest_j = 1000

for search_lat in model_lat:
    for search_lon in model_lon:
        if search_lat > (DP_lat - tol) and search_lat < (DP_lat + tol):
            if search_lon > (DP_lon - tol) and search_lon < (DP_lon + tol):
                dist_DP = math.sqrt((DP_lon - search_lon)**2 + (DP_lat - search_lat)**2) 
                
                if dist_DP < closest_dist:
                    closest_dist = dist_DP
                    closest_lat = search_lat
                    closest_lon = search_lon

print ' '
print 'Model Closest lat: ', closest_lat
print 'Model Closest lon: ', closest_lon

## Extract data from model for the appropriate time series - Arcpy
coords = "lat " + str(closest_lat) + ";lon " + str(closest_lon)

out_csv_file =  "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\testlatlon.xls"



# Process: Make NetCDF Table View
arcpy.MakeNetCDFTableView_md(file, "uas", "raw_table", "time", coords, "BY_VALUE")


# Process: Table To CSV
arcpy.TableToExcel_conversion("raw_table", out_csv_file, "ALIAS", "CODE")   

#current problem: not getting access to the output table for 