"""
capitalize.py

A simple Python script to capitalize the country names.
"""

import csv

data_file = open('html/vis/data.tsv', 'rt')
data_out = open('html/vis/data_out.tsv', 'wt')
csv_reader = csv.reader(data_file)
csv_writer = csv.writer(data_out)

for line in csv_reader:
	print(line[2])
	line[2] = line[2].capitalize()
	csv_writer.writerow([arr for arr in line])