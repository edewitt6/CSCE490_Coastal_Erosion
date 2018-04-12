import netCDF4 
import numpy as np
import math
import csv
import os
import datetime 
from datetime import date

from netCDF4 import Dataset

os.chdir("C:\\Civil Engineering\\Grad School\\699 - Thesis\\Trail Scripts")

file = "C:\\Users\\Euan-Angus MacLeod\\Downloads\\tslsi_3hr_MRI-CGCM3_historical_r1i1p1_200501010000-200512312100.nc"

nc = Dataset(file,'r')

tslsi = nc.variables['tslsi']
lat = nc.variables['lat']
lon = nc.variables['lon']
time = nc.variables['time']

print tslsi
print lat
print lon
print time

#Barter island
BI_lat = 70.133045
BI_lon = (360 - 143.641854) #-143.641854


#for i in range(len(lat)):
    #print "lat: ", lat[i]
    #print "lon: ", lon[i]
#for i in range(len(time)):
    #print time[i]


MRI_lat = lat[:]
MRI_lon = lon[:]

abs_lat_arr = []
abs_lon_arr = []

# to find the closest point to Location
for i in range(len(MRI_lat)):
    abs_lat = abs(MRI_lat[i] - BI_lat)
    abs_lat_arr.append(abs_lat)
 
for j in range(len(MRI_lon)):
    abs_lon = abs(MRI_lon[j] - BI_lon)
    abs_lon_arr.append(abs_lon)
    
#find poistion of min 
min_lat = abs_lat_arr.index(min(abs_lat_arr))
min_lon = abs_lon_arr.index(min(abs_lon_arr))

near_BI_lat = MRI_lat[min_lat]
near_BI_lon = MRI_lon[min_lon]

print ' '
print 'MRI Closest lat: ', near_BI_lat
print 'MRI Closest lon: ', near_BI_lon

# Extract the temp data

#strt_date = time.index(1979-01-01)


#tslsi_BI_ts = tslsi[:, near_BI_lat, near_BI_lon]


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
    wr.writerows(tslsi[2900, near_BI_lat, near_BI_lon])
