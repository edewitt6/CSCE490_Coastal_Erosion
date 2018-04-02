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
import datetime 
from datetime import date

from netCDF4 import Dataset

os.chdir("C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Scripts")

file = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\CSCE690_ Coastal Project\\Data\\SST\\Historical\\CNRM_hist\\CNRM_hist\\tos_Omon_CNRM-CM5_historical_r1i1p1_197001-197912.nc"

nc = Dataset(file,'r')

tos = nc.variables['tos']
lat = nc.variables['lat']
lon = nc.variables['lon']
time = nc.variables['time']

print tos
print lat
print lon
print time

#Drew Point - Units: Decimal Degrees
DP_lat = 70.879
DP_lon = (360 - 153.932) #-153.932



##test for index / lat/lon - Identifies the points closest to the site
CNRM_pnts = np.empty([1,4])

print 'Closest points to Drew Point:'
for i in range(len(lat)):
    for j in range(len(lon)):
        if lat[i][j] > (DP_lat - 1) and lat[i][j] < (DP_lat + 1):
            if lon[i][j] > (DP_lon - 1) and lon[i][j] < (DP_lon + 1):
                
                print 'Lat:', lat[i][j], 'Lon:', lon[i][j], 'i:', i, 'j:', j
                
                CNRM_pnts_row = np.array([lat[i][j],lon[i][j], i, j])
                
                CNRM_pnts = np.vstack((CNRM_pnts, CNRM_pnts_row))
                
                #stack the each line of results to the empty array above 
CNRM_pnts = np.delete(CNRM_pnts, (0), 0)
print ' '
print 'CNRM_pnts:'
print CNRM_pnts


## Find the closest point

#what I plan on doing here is to compare the DP points to the array of points from the model
#       - create array with subtracted numbers - find min - extract i&j?
#essentially what is below in the second to last section


## Extract data from model for the appropriate time series

#work out the time variable
#extract the data for the location and the appropriate time
#store the data in CSV


## Worked with other model/GCM Variable - disregard at theis point in time

abs_lat_arr = []
abs_lon_arr = []

# to find the closest point to Location // THIS MAY NOT WORK FOR THIS DUE TO THE INDEING OF THIS MODEL OUTPUT
for i in range(len(CNRM_lat)):
    abs_lat = abs(CNRM_lat[i] - DP_lat)
    abs_lat_arr.append(abs_lat)
 
for j in range(len(CNRM_lon)):
    abs_lon = abs(CNRM_lon[j] - DP_lon)
    abs_lon_arr.append(abs_lon)
    
#find poistion of min 
min_lat = abs_lat_arr.index(min(abs_lat_arr))
min_lon = abs_lon_arr.index(min(abs_lon_arr))

near_DP_lat = CNRM_lat[min_lat]
near_DP_lon = CNRM_lon[min_lon]

print ' '
print 'CNRM Closest lat: ', near_DP_lat
print 'CNRM Closest lon: ', near_DP_lon

# Extract the temp data

#strt_date = time.index(1979-01-01)


#tos_DP_ts = tslsi[:, near_DP_lat, near_DP_lon]


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
