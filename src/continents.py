"""
continents.py

Adds the continent to the countries listed in data.csv
"""

import csv

continents = ["africa", "asia", "europe", "north_america", "oceania", "south_america"]
continent_dict = {}

# Get the list of countries in each continent. The list of countries in each continent
# have been obtained from world atlas, and stored in txt files under data/continents/
for c in continents:
	c_file = open("data/continents/" + c + ".txt")
	c_list = []
	for line in c_file:
		c_list.append(line.strip().lower())
	continent_dict[c] = c_list

# Now, read the data.csv file and add the continent column.
input_file = open("html/vis/data.csv", "rt")
output_file = open("html/vis/new_data.csv", "wt")

csv_reader = csv.reader(input_file)
next(csv_reader, None)
csv_writer = csv.writer(output_file)

csv_writer.writerow(['id', 'code', 'country', 'gdp', 'edits', 'gdpedits', 'population', 'editspopulation', 'citations', 'fsize', 'links', 'continent'])

# Assign the continents
for line in csv_reader:
	row = [x for x in line]
	for c in continents:
		if line[2].strip().lower() in continent_dict[c]:
			row.append(c)
			break

	csv_writer.writerow(row)