# Created by Euan-Angus MacLeod
#
#Description: This code attempts to extract the lat, lon and the corresponding indices that store the environmental data
#input: tos_Omon_GFDL-CM3_historical_r1i1p1_197501-197912.nc
#output: SST_SP.csv
######################################


import netCDF4 
import numpy as np
import math
import csv
import os
import datetime 
from datetime import date

from netCDF4 import Dataset

os.chdir("C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Scripts")

file = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\Data\\GCM Data\\Non-ESM\\Historical\\GFDL-CM3\\tos_Omon_GFDL-CM3_historical_r1i1p1_197501-197912.nc"

nc = Dataset(file,'r')

tos = nc.variables['tos']
lat = nc.variables['lat']
lon = nc.variables['lon']
time = nc.variables['time']

print tos
print lat
print lon
print time

## rlat?

for i in range(len(lat)):
    for j in range(len(lon)):
        print 'Lat:', lat[i][j], 'Lon:', lon[i][j], 'rlat:', i, 'rlon:', j
        
        
## Find Model Data Location
#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932

s_tol = 5 #search tolerance

model_pnts = np.empty([1,4])

#this is not quite workign yet
#the length of the lat variable is ot the same as the length of the index rlat - how do i find the length of the index?

print 'Closest points to Drew Point:'
for rlat in range(len(lat)):
    for rlon in range(len(lon)):
        if lat[rlat][rlon] > (DP_lat - s_tol) and lat[rlat][rlon] < (DP_lat + s_tol):
            if lon[rlat][rlon] > (DP_lon - s_tol) and lon[rlat][rlon] < (DP_lon + s_tol):
                
                print 'Lat:', lat[rlat][rlon], 'Lon:', lon[rlat][rlon], 'rlat:', rlat, 'rlon:', rlon
                
                model_pnts_row = np.array([lat[rlat][rlon],lon[rlat][rlon], rlat, rlon])
                
                model_pnts = np.vstack((model_pnts, model_pnts_row))
                
                #stack the each line of results to the empty array above 
model_pnts = np.delete(model_pnts, (0), 0)
print ' '
print 'model_pnts:'
print model_pnts


## Finding model location for regular lat and lon
#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932

model_lat = lat[:]
model_lon = lon[:]

abs_lat_arr = []
abs_lon_arr = []

# to find the closest point to Location // THIS MAY NOT WORK FOR THIS DUE TO THE INDEING OF THIS MODEL OUTPUT
for i in range(len(model_lat)):
    abs_lat = abs(model_lat[i] - DP_lat)
    abs_lat_arr.append(abs_lat)
 
for j in range(len(model_lon)):
    abs_lon = abs(model_lon[j] - DP_lon)
    abs_lon_arr.append(abs_lon)
    
#find poistion of min 
min_lat = abs_lat_arr.index(min(abs_lat_arr))
min_lon = abs_lon_arr.index(min(abs_lon_arr))

near_DP_lat = model_lat[min_lat]
near_DP_lon = model_lon[min_lon]

print ' '
print 'Model Closest lat: ', near_DP_lat
print 'Model Closest lon: ', near_DP_lon

## Extract the uas data

#strt_date = time.index(1979-01-01)
#current problem with the time: the count is days since 1860-01-01 00:00:00 in 0.125 increments (3hrs)

uas_DP_ts = uas[:, near_DP_lat, near_DP_lon]


## Write the lat/lon to file

with open('Lat.csv', 'w') as latfile:
    wr = csv.writer(latfile)
    wr.writerow(lat[:])

    
with open('Lon.csv', 'w') as lonfile:
    wr = csv.writer(lonfile)
    wr.writerows(lon[:])
    
##
with open('tslsi.csv', 'w') as tempfile:
    wr = csv.writer(tempfile)
    wr.writerows(tslsi[2900, near_DP_lat, near_DP_lon])
