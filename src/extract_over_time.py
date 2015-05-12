'''
extract_over_time.py

Given a dense file organized by country by line,
extracts the hard-coded feature over time by summing up the values
'''
import os
import csv
import sys

fd = open(sys.argv[1])
feature_col = 3
reader = csv.reader(fd)

reader.next() # skip header

country_list = []

for line in reader:
    if country_list == []:
        country_list = line # First case, sum is just first line
    else:
        for i in range(2,len(country_list)):
            if float(country_list[i]) == -1: # If data is not there (from dense data)
                country_list[i] = 0 #Set it to zero, should only really happen after the first iteration
            if not line[i] == "-1": # If actual data
                country_list[i] = float(country_list[i]) + float(line[i]) #Add it

country_list[0] = os.path.basename(sys.argv[1]) #Reset name
print "\t".join([str(i) for i in country_list])
