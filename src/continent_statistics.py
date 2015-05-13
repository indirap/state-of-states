"""
continent_statistics.py
Gets the average and sum of edits and population per continent.
"""

import csv

continents = ["africa", "asia", "europe", "north_america", "oceania", "south_america"]

# Read the data.csv file and get the number of edits for each continent
continent_sum = {}
continent_num = {}
continent_pop = {}
for c in continents:
	continent_sum[c] = 0
	continent_num[c] = 0
	continent_pop[c] = 0

input_file = open("html/vis/data.csv", "rt")
csv_reader = csv.reader(input_file)
next(csv_reader, None)

for line in csv_reader:
	if line[4] != "":
		continent_sum[line[11]] += float(line[4])
		continent_num[line[11]] += 1
	if line[6] != "":
		continent_pop[line[11]] += float(line[6])

# Calculate the averages
continent_avg = {}
continent_editsperpop = {}

for c in continent_sum:
	continent_avg[c] = continent_sum[c]/continent_num[c]
	continent_editsperpop[c] = continent_sum[c]/continent_pop[c]
	print(c + "; average: " + str(continent_avg[c]) + "; edits per population: " + str(continent_editsperpop[c]))

# Write to file
output_file = open("html/vis/continent_data.csv", "wt")
csv_writer = csv.writer(output_file)
# Write the header
csv_writer.writerow(['id', 'continent', 'average_edits', 'sum_edits', 'sum_population', 'edits_per_population'])

input_file = open("html/vis/data.csv", "rt")
csv_reader = csv.reader(input_file)
next(csv_reader, None)
for line in csv_reader:
	c = line[11]
	csv_writer.writerow([line[0], c, continent_avg[c], continent_sum[c], continent_pop[c], continent_editsperpop[c]])