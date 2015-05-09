import os
import csv
import sys

#feature = sys.argv[3]
fd = open(sys.argv[1])

feature_col = 3

'''
if(feature == "citations"):
    feature_col = 3
elif feature == "size":
    feature_col = 4
elif feature == "links":
    feature_col = 5
'''


reader = csv.reader(fd)

reader.next() # skip header

name = sys.argv[1] # Country Name
country_list = []

for line in reader:
    #list_line = list(line)
    if country_list == []:
        country_list = line
    else:
        for i in range(2,len(country_list)):
            if float(country_list[i]) == -1:
                country_list[i] = 0
            if not line[i] == "-1":
                country_list[i] = float(country_list[i]) + float(line[i])

country_list[0] = os.path.basename(sys.argv[1])

print "\t".join([str(i) for i in country_list])
#print os.path.basename(sys.argv[3])+"\t"+ str(citation_val)+"\t"+str(size_val)+"\t"+str(link_val)
