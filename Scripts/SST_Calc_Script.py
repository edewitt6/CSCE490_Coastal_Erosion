# Author: Eric DeWitt
# Date 28 April 2018
# Purpose:   For each model:
#       Read in observed data (csv)
#       Read in historic data (csv)
#       For each of the rows in the time series for the same period find the difference
#             Diff = Observed value - GCM value
#       For each month increment, average the difference
#             Month: average every diff value for Jan ,feb , march, etc..
#       Read in projected data
#       For each row of time series, apply the averaged value
#             GCM projected value + averaged difference
#       Output the projected time series (csv)
#             Average the output for each of the model
#       Arithmetic mean of each row of the time series
#       Output combined time series (csv)

import arcpy
import csv
import math
import os
import sys
from arcpy import env

path = "C:\Users\edewi_000\Desktop\Coastal Errosion\Results\SST"
os.chdir(path)
env.workspace = path

# Convert Celsius to Kelvin
def to_kelvin(degree):
    kelvin = float(float(degree) + 273.15)
    return kelvin

# Some lists used
file1 = "DP_Obs_SST.csv"
kelvin_list = []
hist_temp_list = []
diff_list = []
file_list = []
proj_file_list = []
avg_list = []

# Takes values from the Obs_SST file and converts to Kelvin and appends to a list
def append_kelvin_list():    
    with open(file1, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Year'] == '2006':
                break
            else:
                kelvin_list.append(to_kelvin(row['SST (C)']))
 
# Creates lists of historical and projected files               
def append_file_list():
    for files in os.listdir(path):
        if 'historical' in files and files.endswith('csv'):
            file_list.append(files)
        elif 'rcp85' in files and files.endswith('csv'):
            proj_file_list.append(files) 

# Creates a list of difference values from the observed - historical data sets from 1979-2005 
def append_diff_list():
    # loop through each historical file and find the object that corresponds with each item in kelvin list
    index = 0
    date_range = range(1979,2006)
    for file in file_list:
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            print ("checking file: ", file)
            for row in reader:
                for date in date_range:
                    if str(date) in row['time']:
                        #print "\t", date, " in ", row['time']
                        d = kelvin_list[index] - float(row['tos'])
                        diff_list.append(d)
                        index += 1

# Creates a list of difference averages for each month from 1979-2005
def append_avg_list():
    # loop through the diff_list and get the avg diff for each mo
    # avg_list is a 12 item list with the avg diff for each mo
    # there are 324 items in diff_list. So 324/12 = 27
    # the formula for the index of each mo would be:
    #   (mo-1) + (12 * range(0,27))
    # the avg would be the sum of those values found /27
    
    for month in range(0,12):
        sum = 0
        for i in range(0,27):
            index = month + (12*i)
            sum = sum + (diff_list[index])
        avg = sum/27
        avg_list.append(avg)


def make_csv(file_name,proj,time_a):
    with open(file_name, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, ['time','tos'],delimiter = ",")
        writer.writeheader()
        for i in range(len(proj)):
            writer.writerow({'time': time_a[i],'tos': proj[i]})
       
def add_avg_to_proj():
    # loop through projected data and add the avg diff to each mo
    # then create a composite csv file with new data
    for file in proj_file_list:
        index = 0
        new_file = "NEW_" + str(file)
        new_projection = []
        time_array = []
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_projection.append(float(row['tos']) + avg_list[index])
                time_array.append(row['time'])
                index += 1
                if index == 12:
                    index = 0
        make_csv(new_file,new_projection,time_array)

append_kelvin_list()
append_file_list()
append_diff_list()
append_avg_list()
add_avg_to_proj()
#print kelvin_list
#print file_list
#print diff_list
#print avg_list