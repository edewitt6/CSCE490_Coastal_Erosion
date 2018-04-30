# Derek Tengwall
# April 28th
# Purpose: extract the magnitude variable of uas and vas and get the resultant magnitude and bearing # and output to new csv file
# import this modules and pass it the names of the extracted uas and vas csv files

import csv
from math import hypot, atan2, degrees

def Merger(uasfile, vasfile):
    uas_list = []
    # list  field names to print in output
    field_list = ["OID","Time","UAS","VAS","Magnitude","Corrected Bearing"]
    out_file = "Wind_" + uasfile[6:-4]+ ".csv" # grabs the year of the files being processed

    ## opens uas input csv
    try:
        with open(uasfile) as uasFile: 
        # opens vas input csv
            with open(vasfile) as vasFile:
                ## opens output csv file
                 with open(out_file, 'wb') as csvOFile:
                    writer = csv.writer(csvOFile, delimiter=',', quotechar='"')
                    writer.writerow(field_list)
                    reader1 = csv.DictReader(uasFile)
                    reader2 = csv.DictReader(vasFile)
                    for row in reader1:
                        uas_list.append(row['uas']) # grabs the uas values from first csv
                    count = 0
                    for row2 in reader2:
                    #puts everything together while extrcting and writing to output csv file
                        uas = float(uas_list[count])
                        vas = float(row2['vas'])
                        magnitude = hypot(uas, vas)
                        bearing = float(atan2(vas , uas))
                        bearing = degrees(bearing) + 270
                        writer.writerow([row2['OID'] , row2['time'], uas, vas, magnitude, bearing])
                        count = count + 1
                        
                        
    except IOError:
        print("\nSST_MERGE ERROR:An error occured reading the file. make sure the file extension was input as well(.csv)")
    except KeyError:
        print("\nSST_MERGE ERROR:This error means you probably spelled the field names wrong. try again")
    
