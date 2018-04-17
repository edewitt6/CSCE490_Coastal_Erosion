# Created by Euan-Angus MacLeod
#
#Description: This code attempts to extract the lat, lon and the corresponding indices that store the environmental data
#input: tos_Omon_GFDL-CM3_historical_r1i1p1_197501-197912.nc
#output: SST_SP.csv
######################################

import os
import arcpy
import netCDF4 
from netCDF4 import Dataset

from arcpy import env
path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project"
env.workspace = path
env.scratchWorkspace = path
env.overwriteOutput = True


site = "DP" #DP: Drew Point; O: Oliktok; BI:Barter Island

#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = -153.932 #(360 - 153.932) #-153.932

s_tol = 1 #search tolerance

closest_dist = 10000000000000000000000
closest_rlat = 1000
closest_rlon = 1000
closest_indx_rlat = 1000
closest_indx_rlon = 1000

main_dir = 'C:\\Users\\Euan-Angus MacLeod\\Google Drive\\Data\\GCM Data\\Non-ESM\\RCP85\\GFDL-CM3'
#main_dir = 'C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic\\Ua'

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
    rlat = nc.variables['rlat']
    rlon = nc.variables['rlon']
    model_rlat = rlat[:]
    model_rlon = rlon[:]
    
    # print tos
    # print lat
    # print lon
    # print time
    
    print 'Extracting:', file_name, '\n'   
    
    
    #Find Model Data Location
    
    print 'Calculating closest model point to Drew Point in', file_name, '\n'
    for rlat in range(lat.shape[0]):
        for rlon in range(lon.shape[1]):
            if lat[rlat][rlon] > (DP_lat - s_tol) and lat[rlat][rlon] < (DP_lat + s_tol):
                #print 'lat:', lat[rlat][rlon]
                if lon[rlat][rlon] > (DP_lon - s_tol) and lon[rlat][rlon] < (DP_lon + s_tol):
                    #print 'lon: ',  lon[rlat][rlon]
                    dist_DP = math.sqrt((DP_lon - lon[rlat][rlon])**2 + (DP_lat - lat[rlat][rlon])**2) 
                    
                    if dist_DP < closest_dist:
                        closest_dist = dist_DP
                        closest_indx_rlat = rlat
                        closest_indx_rlon = rlon
                        closest_rlat = model_rlat[rlat]
                        closest_rlon = model_rlon[rlon]
                        
                    #print 'Lat:', lat[rlat][rlon], 'Lon:', lon[rlat][rlon], 'rlat:', model_rlat[rlat], 'rlon:', model_rlon[rlon]
        
    print 'Closest model point to Drew Point:'
    print 'Lat:', lat[closest_indx_rlat][closest_indx_rlon], 'Lon:', lon[closest_indx_rlat][closest_indx_rlon], 'rlat:', closest_rlat, 'rlon:', closest_rlon, '\n'
    
    
    # Extract data from model for the appropriate time series - Arcpy
    
    coords = "rlat " + str(closest_rlat) + ";rlon " + str(closest_rlon)
    
    out_csv_file =  output_dir + "\\" +  site + "_" + file_name + ".xls"
    
    
    
    # Process: Make NetCDF Table View
    arcpy.MakeNetCDFTableView_md(file, "tos", "raw_table", "time", "rlon -153.5;rlat 72.500001", "BY_VALUE")
    
    print 'Extracted data written to', out_csv_file, '\n'
    # Process: Table To CSV
    arcpy.TableToExcel_conversion("raw_table", out_csv_file, "ALIAS", "CODE")   
    


