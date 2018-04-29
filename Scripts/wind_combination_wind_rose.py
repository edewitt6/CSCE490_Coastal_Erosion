#Author: EA MacLeod
#Date: 4/25/18
#Purpose: Combines two component vectos into one resultant wind vector and two wind directions

import csv
import numpy as np
import os
import math as m


# initialize some empty lists
time = []
ua = []
va = []
w_mag = []
w_dir_v = []
w_dir_m = []
wind_evnt_all = np.array(["time", "Ua", "Va", "w_mag", "w_dir_vector", "w_dir_met"])
wind_evnt_row = []



ua_base_file_path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic\\CSV_Results\\ua"
va_base_file_path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic\\CSV_Results\\va"
results_file_path = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\Wind_Script_Results"


for ua_file_name in os.listdir(ua_base_file_path):

    #ua_file_name = "C:\\Users\\Euan-Angus MacLeod\\Google Drive\\DP_GCM_Wind\\GFDL_NC\\Historic\\Results\\BI_uas_00-04.xls"

    ua_file = ua_base_file_path + '\\' + ua_file_name
    
    va_file_name = ua_file_name.replace('uas', 'vas')
    
    va_file = va_base_file_path + '\\' + va_file_name
    
    with open(ua_file, 'r') as ua_csvfile:
        ua_reader = csv.reader(ua_csvfile, delimiter=',')
        ua_header = ua_reader.next() # read first line as header
        row_num = 0
        
        for row in ua_reader:
            ua.append(float(row[2]))
            time.append(row[1])
        
    with open(va_file, 'r') as va_csvfile:
        va_reader = csv.reader(va_csvfile, delimiter=',')
        va_header = va_reader.next() # read first line as header
        row_num = 0 
        
        for row in va_reader:
            va.append(float(row[2]))
        


for (indx, x) in enumerate(range(len(time))):
    #Calculate wind mag, m/s
    w_mag_unit = m.sqrt(ua[x]**2 + va[x]**2)
    
    
    #Calculate wind dir, both vector azimuth and meteorological conventions
    w_dir_v_unit = m.degrees(m.atan2(ua[x], va[x]))
    
    # wind vector azimuth
    if w_dir_v_unit < 0:
        w_dir_v_unit = w_dir_v_unit + 360
        
    # meteorological convention
    w_dir_m_unit = m.degrees(m.atan2(-ua[x], -va[x]))
    
    if w_dir_m_unit < 0:
        w_dir_m_unit = w_dir_m_unit + 360
    
    time_unit = time[x]
        
    w_mag.append(w_mag_unit)
    w_dir_v.append(w_dir_v_unit)
    w_dir_m.append(w_dir_v_unit)
    
    wind_evnt_row = np.array([time_unit, ua[x], va[x], w_mag_unit, w_dir_v_unit, w_dir_m_unit])
    
    wind_evnt_all = np.vstack((wind_evnt_all, wind_evnt_row))
    
    #% complete
    perc = int((float(indx) / float(len(time))) * 100)
    print str(perc) + '% complete'


os.chdir(results_file_path)
doc_strm_val = 'wind_values.csv'
with open(doc_strm_val , 'w') as tempfile:
    wr = csv.writer(tempfile)              
    
    for i in range(np.size(wind_evnt_all, 0)):
        wr.writerows([wind_evnt_all[i, :]]) 
        
## wind rose
import windrose
import random
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from numpy import arange

#Create wind speed and direction variables
# ws = random.randint(1,500)*6
# wd = random(500)*360

#A quick way to create new windrose axes...
def new_axes():
    fig = plt.figure(figsize=(8, 8), dpi=80, facecolor='w', edgecolor='w')
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(fig, rect, axisbg='w')
    fig.add_axes(ax)
    return ax

#...and adjust the legend box
def set_legend(ax):
    l = ax.legend()
    plt.setp(l.get_texts(), fontsize=8)

# A stacked histogram with normed (displayed in percent) results :
# 
ax = new_axes()
ax.bar(w_dir_m, w_mag, normed=True, opening=0.8, edgecolor='white')
set_legend(ax)
plt.show()
