# Author: Derek Tengwall
# Date: 14 April 2018
# Purpose: Averages values given the csv column names

import csv


input_csv = raw_input("Type name of input file(example.csv):")
type(input_csv)

col1 = raw_input("Type first field name to average:")
type(col1)

col2 = raw_input("Type second field name to average:")
type(col2)

out_file = raw_input("Type the desired name of output file:")
type(out_file)
## opens input csv
try:
    with open(input_csv) as csvIFile: 
        ## opens output csv file
        with open(out_file, 'wb') as csvOFile:
            writer = csv.writer(csvOFile, delimiter=',', quotechar='"')
            writer.writerow([col1,col2,'Average'])
            reader = csv.DictReader(csvIFile)
            for row in reader:
                average = float((float(row[col1]) + float(row[col2])) /2)
                writer.writerow([row[col1],row[col2],average])
except IOError:
    print("\nAn error occured reading the file. make sure the file extension was input as well(.csv)")
except KeyError:
    print("\nThis error means you probably spelled the field names wrong. try again")
print("\nDONE!")