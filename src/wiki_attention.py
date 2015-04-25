"""
wiki_attention.py

Calculates the amount of attention a particular country has. This takes into account:
-	Number of pageviews. (Not sure how to get the data though)
-	Number of edits. [Maybe read the [country]_data.csv files to get the number of edits?]
-	Number of backlinks. [Not sure how?]
-	Length of page. [DONE]
-	Number of citations. [DONE]

Right now it only takes into account the file sizes of the pages.
"""

import os
import csv

country_data = open('data/countries.txt', 'r')
for country in country_data:
	dirpath = "./data/testing-countries/" + country.strip() + "/"

	country_size = 0
	country_pages = 0

	for dirname, dirnames, filenames in os.walk(dirpath):

		if len(filenames) != 0:
			country_f = open('data/' + country + '_data.csv', 'wt')
			csv_writer = csv.writer(country_f)
			csv_writer.writerow(('filename', 'year', 'month', 'num_citations', 'file_size'))

		# print path to all filenames.
		for filename in filenames:
			# Need to get the month and the year
			array = filename.split('-')
			year = int(array[len(array)-3])
			month = int(array[len(array)-2])
			title = ""
			for num in range(len(array)-3):
				title += array[num] + " "
			title = title.strip()
			title = title.replace('_', ' ')
			print(title + " - " + str(year) + "-" + str(month))

			print(os.path.join(dirname, filename) + " " + str(os.path.getsize(os.path.join(dirname, filename))))
			country_size += os.path.getsize(os.path.join(dirname, filename))
			country_pages += 1

			num_citations = 0
			with open(os.path.join(dirname, filename)) as f:
				for line in f:
					if "reference-text" in line:
						num_citations += 1

			print("num_citations: " + str(num_citations))

			csv_writer.writerow((title, year, month, num_citations, os.path.getsize(os.path.join(dirname, filename))))