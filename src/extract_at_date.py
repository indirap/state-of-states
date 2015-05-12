'''
extract_at_date.py

Given a csv file containing all of the countries by line,
selects the hard-coded feature at a given year and month.
The file name is passed in
The filtered output is printed to stdin.
'''
import os
import csv
import sys

y = sys.argv[1]
m = sys.argv[2]
fd = open(sys.argv[3])

feature_col = 3


reader = csv.reader(fd)

citation_val = 0
size_val = 0
link_val = 0

for line in reader:
    if line[1] == y and line[2] == m:
        citation_val += int(line[3])
        size_val += int(line[4])
        link_val += int(line[5])

print os.path.basename(sys.argv[3])+"\t"+ str(citation_val)+"\t"+str(size_val)+"\t"+str(link_val)
