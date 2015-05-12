"""
wiki_attention.py

Calculates the amount of attention a particular country has. This takes into account:
-	Number of edits.
-	Number of forward links.
-	Length of page.
-	Number of citations.

Right now it only takes into account the file sizes of the pages.
"""

import os
import csv
import re
from bs4 import BeautifulSoup

# countries.txt is a txt file containing the names of all countries we
# downloaded from Wikipedia. 
country_data = open('data/country_name_data/countries.txt', 'r')
for country in country_data:
		print "Starting %s" % country.strip()

	dirpath = "./data/downloaded_pages/" + country.strip() + "/"
	dirpath = dirpath.replace(" ", "_")

	country_size = 0
	country_pages = 0

	# Traverse all the Wikipedia pages associated with each path, and write
	# to a CSV file the filename, year, month, number of citations, file size
	# as well as forward links from that page.
	for dirname, dirnames, filenames in os.walk(dirpath):
		if len(filenames) != 0:
			country_f = open('data/country_data/' + country.strip() + '_data.csv', 'wt')
			csv_writer = csv.writer(country_f)
			csv_writer.writerow(('filename', 'year', 'month', 'num_citations', 'file_size', 'forward_links'))

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

			country_size += os.path.getsize(os.path.join(dirname, filename))
			country_pages += 1

			num_citations = 0

			# Count number of citations and forward links. Only count the forward links
			# if they point to other Wikipedia pages. 
			with open(os.path.join(dirname, filename)) as f:
				for line in f:
					if "reference-text" in line:
						num_citations += 1

						# Forward links
						forward_links = []
						num_forward_links = 0
						with open(os.path.join(dirname, filename)) as f:
							soup = BeautifulSoup(f)
							wiki_links = soup.find_all('a', href=re.compile("^/wiki/"))
							for link in wiki_links:
								if not 'Portal:' in link['href']:
									forward_links.append(link)
						num_forward_links = len(forward_links)

			csv_writer.writerow((title, year, month, num_citations, os.path.getsize(os.path.join(dirname, filename)), num_forward_links))