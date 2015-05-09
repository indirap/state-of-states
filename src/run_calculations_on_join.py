import os
import sys
import csv
import scipy.stats

# Takes a joined data set and calculates pearson correlation on data

# Load data

gdp_data = []
citation_data = []
fsize_data = []
link_data = []


fd = open(sys.argv[1], 'r')
reader = csv.reader(fd, delimiter='\t')

reader.next()

for line in reader:
    if line[3] =="":
        continue
    gdp_data.append(float(line[3]))
    citation_data.append(int(line[4]))
    fsize_data.append(int(line[5]))
    link_data.append(int(line[6]))

#Correlate
print sys.argv[1] + "\tCitation\t" + str(scipy.stats.pearsonr(gdp_data, citation_data)[0])
print sys.argv[1] + "\tFile Size\t" + str(scipy.stats.pearsonr(gdp_data, fsize_data)[0])
print sys.argv[1] + "\tLinks\t" + str(scipy.stats.pearsonr(gdp_data, link_data)[0])
