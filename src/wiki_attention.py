"""
wiki_attention.py

Calculates the amount of attention a particular country has. This takes into account:
-	Number of pageviews. (Not sure how to get the data though)
-	Number of edits.
-	Number of backlinks.
-	Length of page.
-	Number of citations.

Right now it only takes into account the file sizes of the pages.
"""

import os

country_dict = {}
country_data = open('data/countries.txt', 'r')
for country in country_data:
	print (country.strip())
	country_dict[country.strip()] = 0

for country in country_dict:
	dirpath = "./data/testing-countries/" + country + "/"

	country_size = 0
	country_pages = 0

	for dirname, dirnames, filenames in os.walk(dirpath):

		# print path to all subdirectories first.
		for subdirname in dirnames:
			print(os.path.join(dirname, subdirname))

		# print path to all filenames.
		for filename in filenames:
			print(os.path.join(dirname, filename) + " " + str(os.path.getsize(os.path.join(dirname, filename))))
			country_size += os.path.getsize(os.path.join(dirname, filename))
			country_pages += 1

	if country_size != 0:
		country_dict[country] = float(country_size)/country_pages

for country in country_dict:
	if country_dict[country] != 0:
		print(country + " " + str(country_dict[country]))