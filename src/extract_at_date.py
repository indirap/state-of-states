import os
import csv
import sys

y = sys.argv[1]
m = sys.argv[2]
#feature = sys.argv[3]
fd = open(sys.argv[3])

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

citation_val = 0
size_val = 0
link_val = 0

for line in reader:
    if line[1] == y and line[2] == m:
        citation_val += int(line[3])
        size_val += int(line[4])
        link_val += int(line[5])

print os.path.basename(sys.argv[3])+"\t"+ str(citation_val)+"\t"+str(size_val)+"\t"+str(link_val)
