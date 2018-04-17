# Created by Euan-Angus MacLeod
#
#Description: This code attempts to extract the lat, lon and the corresponding indices that store the environmental data
#input: uas_3hr_GFDL-CM3_historical_r1i1p1_1975010100-1979123123.nc
#output: SST_SP.csv
######################################


import netCDF4 
from netCDF4 import Dataset
import os
import arcpy

from arcpy import env
path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project"
env.workspace = path
env.scratchWorkspace = path
env.overwriteOutput = True


site = "DP" #DP: Drew Point; O: Oliktok; BI:Barter Island

#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932


tol = 1 #search tolerance (decimal degree)

closest_dist = 10000000000000000000000
closest_lat = 1000
closest_lon = 1000

main_dir = 'C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic\\Ua'
output_dir = 'C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic'

# for folder_name in os.listdir(main_dir):
#     #print folder_name
#     folder_path = main_dir + '\\' + folder_name
    
    #start NetCDF data extraction
for file_name in os.listdir(main_dir):

    print'---------------------------------------------'

    file = main_dir + '\\' + file_name #add if the loop above is used:  '\\' + folder_name +

    nc = Dataset(file,'r')
    
    uas = nc.variables['uas']
    lat = nc.variables['lat']
    lon = nc.variables['lon']
    time = nc.variables['time']
    
    # print uas
    # print lat
    # print lon
    # print time
    
    model_lat = lat[:]
    model_lon = lon[:]
    
    # Find Model Data Location
    
    print 'Calculating closest model point to Drew Point in', file_name, '\n'
    
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
    print 'Closest model point to Drew Point:'
    print 'Lat:', closest_lat, 'Lon:', closest_lon, '\n'
    
    # Extract data from model for the appropriate time series - Arcpy
    coords = "lat " + str(closest_lat) + ";lon " + str(closest_lon)
    
    out_csv_file =  output_dir + "\\" +  site + "_" + file_name + ".xls"
    
    
    # Process: Make NetCDF Table View
    arcpy.MakeNetCDFTableView_md(file, "uas", "raw_table", "time", coords, "BY_VALUE")
    
    print 'Extracted data written to \n', out_csv_file, '\n'
    # Process: Table To CSV
    arcpy.TableToExcel_conversion("raw_table", out_csv_file, "ALIAS", "CODE")   

