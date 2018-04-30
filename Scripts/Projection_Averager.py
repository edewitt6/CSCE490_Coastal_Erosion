# Author: Eric DeWitt
# Date: 29 April 2018
# Purpose: Get averages for each projection model and write to a new csv file with the averaged data
import os

path = "C:\Users\edewi_000\Desktop\Coastal Errosion\Results\NEW_Projection"
os.chdir(path)

model_value_list = []
model_date_list = []
date_range = range(2016,2046)

# Loop through each projected data file and get values
for file in os.listdir(path):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for date in date_range:
                if str(date) in row['time']:
                    model_value_list.append(row['tos'])
                    model_date_list.append(row['time'])

# Only need first 360 values for time
del model_date_list[360:]

# Get averages for each month and year per model
avg_val_list = []
for i in range(len(model_value_list)/4):
    avg = (float(model_value_list[i]) + float(model_value_list[i+360]) + float(model_value_list[i+(360*2)]) + float(model_value_list[i+(360*3)]))/4
    avg_val_list.append(avg)

filename = "AVG_Proj_Value_201601_204512.csv"

# Write values to a csv file
with open(filename, 'wb') as csvfile:
    writer = csv.DictWriter(csvfile,['time','tos'],delimiter = ",")
    for i in range(360):
        writer.writerow({'time':model_date_list[i],'tos':avg_val_list[i]})