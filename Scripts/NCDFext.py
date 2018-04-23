# Author: Eric DeWitt
# Credit: Euan-Angus MacLeod (Extract_test scripts)
# Date: 22 April 2018
# See file_struc.jpeg for file structure needed
# Dependency: x_to_csv.py in root folder of project

import os
import arcpy
import netCDF4 
from netCDF4 import Dataset
from arcpy import env
import sys

path = "C:\Users\edewi_000\Desktop\Coastal Errosion"
sys.path.append(path)
import x_to_csv
env.workspace = path
env.scratchWorkspace = path
env.overwriteOutput = True
out_dir = path + "\\Results"

def main_dir():
    m = input("Enter in directory you want to run in quotations:")
    return m

# DP: Drew Point; O: Oliktok; BI:Barter Island
# Units: Decimal Degrees
class DREW_PNT:
    closest_dist = 10000000000000000000000
    closest_lat = 1000
    closest_lon = 1000
    closest_i = 1000
    closest_j = 1000
    closest_rlat = 1000
    closest_rlon = 1000
    
    lat_Val = []
    lon_val = []
    
    def __init__(self,lon,file_type,site = ("DP"),lat = (70.879),s_tol = (1)):
        self.lon = self.determine_lon(lon)
        self.site = site
        self.lat = lat
        self.s_tol = s_tol
        self.file_type = file_type
    # Determines Longitude value dependent on the file type
    def determine_lon(self,value):
        if value == True:
            return -153.932
        else:
            return 206.068
        
    def print_closest_pnt(self):
        if self.file_type == "uas":
            print "\nClosest model point to Drew Point:\nLat:", self.closest_lat, 'Lon:', self.closest_lon, "\n"
        else:
            print 'Lat:', self.lat_Val[self.closest_i][self.closest_j], 'Lon:', self.lon_Val[self.closest_i][self.closest_j], 'i:', self.closest_i, 'j:', self.closest_j

def net_cdf_extract():
    drew = DREW_PNT(0,0)
    if main.endswith("Ua"):
        drew.file_type = "uas"
        uas_extract(drew)
    elif main.endswith("CNRM_hist"):
        ij_extract(drew)
    elif main.endswith("GFDL-CM3"):
        r_extract(drew)
    x_to_csv.convert(out_dir)
        
def print_Close_Statement(file):
    print 'Calculating closest model point to Drew Point in:', file, '\n'
    
def plat(drew):
    return drew.lat + drew.s_tol
def mlat(drew):
    return drew.lat - drew.s_tol
def mlon(drew):
    return drew.lon - drew.s_tol
def plon(drew):
    return drew.lon + drew.s_tol
def tbl_to_csv(out_csv_file):
    print 'Extracted data written to', out_csv_file, '\n'
    arcpy.TableToExcel_conversion("raw_table", out_csv_file, "ALIAS", "CODE")

def uas_extract(drew):
    for file in os.listdir(main):
        nc = Dataset(file, 'r')
        
        uas = nc.variables['uas']
        lat = nc.variables['lat']
        lon = nc.variables['lon']
        time = nc.variables['time']
        
        model_lat = lat[:]
        model_lon = lon[:]
        
        # Find Model Data Location
        print_Close_Statement(file)
        
        for u_lat in model_lat:
            for u_lon in model_lon:
                if (u_lat > mlat(drew) and u_lat < plat(drew)) and (u_lon > mlon(drew) and u_lon < plon(drew)):
                    dist_DP = math.sqrt((drew.lon - u_lon)**2 + (drew.lat - u_lat)**2)
                    if dist_DP < drew.closest_dist:
                        drew.closest_dist = dist_DP
                        drew.closest_lat = u_lat
                        drew.closest_lon = u_lon
        drew.print_closest_pnt()
        
        #Extract data from model for the appropriate time series - Arcpy
        coords = "lat " + str(drew.closest_lat) + ";lon " + str(drew.closest_lon)
        out_csv_file =  out_dir + "\\" +  drew.site + "_" + file + ".xls"
        
        # Process: Make NetCDF Table View
        arcpy.MakeNetCDFTableView_md(file, "uas", "raw_table", "time", coords, "BY_VALUE")
        tbl_to_csv(out_csv_file)
    
def ij_extract(drew):
    for file in os.listdir(main):
        nc = Dataset(file,'r')
        
        tos = nc.variables['tos']
        drew.lat_Val = nc.variables['lat']
        drew.lon_Val = nc.variables['lon']
        time = nc.variables['time']
        
        print_Close_Statement(file)
        
        for i in range(drew.lat_Val.shape[0]):
            for j in range(drew.lon_Val.shape[1]):
                if (drew.lat_Val[i][j] > mlat(drew) and drew.lat_Val[i][j] < plat(drew)) and (drew.lon_Val[i][j] > mlon(drew) and drew.lon_Val[i][j] < plon(drew)):
                    dist_DP = math.sqrt((drew.lon - drew.lon_Val[i][j])**2 + (drew.lat - drew.lat_Val[i][j])**2) 
                    if dist_DP < drew.closest_dist:
                        drew.closest_dist = dist_DP
                        drew.closest_i = i
                        drew.closest_j = j
        drew.print_closest_pnt()
        
        # Extract data from model for the appropriate time series - Arcpy
        coords = "i " + str(drew.closest_i) + ";j " + str(drew.closest_j)
        out_csv_file =  out_dir + "\\" +  drew.site + "_" + file + ".xls"
        
        # Process: Make NetCDF Table View
        arcpy.MakeNetCDFTableView_md(file, "tos", "raw_table", "time", coords, "BY_VALUE")
        tbl_to_csv(out_csv_file)
    
def r_extract(drew): # Don't know if this works yet as I don't have the files yet with rlat/rlong 
    for file in os.listdir(main):
        nc = Dataset(file,'r')
        
        tos = nc.variables['tos']
        lat = nc.variables['lat']
        lon = nc.variables['lon']
        time = nc.variables['time']
        rlat = nc.variables['rlat']
        rlon = nc.variables['rlon']
        model_rlat = rlat[:]
        model_rlon = rlon[:]
        
        #Find Model Data Location
        print_Close_Statement(file)
        for i in range(lat.shape[0]):
            for j in range(lon.shape[1]):
                if (lat[i][j] > mlat(drew) and lat[i][j] < plat(drew)) and (lon[i][j] > mlon(drew) and lon[i][j] < plon(drew)):
                        dist_DP = math.sqrt((drew.lon - lon[i][j])**2 + (drew.lat - lat[i][j])**2)
                        if dist_DP < closest_dist:
                            drew.closest_dist = dist_DP
                            drew.closest_i = i
                            drew.closest_j = j
                            drew.closest_rlat = model_rlat[i]
                            drew.closest_rlon = model_rlon[j]
            
        print 'Closest model point to Drew Point:'
        print 'Lat:', lat[drew.closest_i][drew.closest_j], 'Lon:', lon[drew.closest_i][drew.closest_j], 'rlat:', drew.closest_rlat, 'rlon:', drew.closest_rlon, '\n'
        
        # Extract data from model for the appropriate time series - Arcpy
        coords = "rlat " + str(drew.closest_rlat) + ";rlon " + str(drew.closest_rlon)
        out_csv_file =  out_dir + "\\" +  drew.site + "_" + file + ".xls"
        
        # Process: Make NetCDF Table View
        arcpy.MakeNetCDFTableView_md(file, "tos", "raw_table", "time", "rlon -153.5;rlat 72.500001", "BY_VALUE")
        tbl_to_csv(out_csv_file)

main = main_dir()
print main
os.chdir(main)

net_cdf_extract()