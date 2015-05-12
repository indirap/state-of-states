"""
wiki_score.py

This Python script reads a sparse matrix describing the different Wikipedia
attention metrics of various countries and outputs a dense matrix of the same
information.
"""

import os
import csv

def sparse_matrix(page_array):
	for year in range(2001, 2016):
		for month in range(12):
			if page_array[year-2001][month] == 0:
				m,y = get_prev_my(month, year)
				if y!=0:
					page_array[year-2001][month] = page_array[y-2001][m]
	return page_array

def get_prev_my(month, year):
	if month>0:
		return (month-1),year
	elif year>2001:
		return 11,(year-1)
	else:
		return 0,0

if __name__ == "__main__":

	# time_array is a 15 by 12 matrix where the rows refer to the years 2001
	# to 2015, and the columns represent each month of the year. This matrix
	# stores the average or sum of the different Wikipedia metrics over all
	# the different Wikipedia pages associated with a country.
	time_array = [[0 for num in range(12)] for num in range(2001,2016)]

	# num_array is similar to time_array, except that instead of storing the
	# different Wikipedia metrics, it stores how many different pages have
	# been read (Grand Duchy of Tuscany in June, 2005 is considered the same
	# page as Grand Duchy of Tuscany in August, 2007, but Grand Duchy of Tuscany
	# in June, 2005 is different from Vienne Summer of Logic in June, 2005).
	num_array = [[0 for num in range(12)] for num in range(2001,2016)]

	# Specifies which country's data to process.
	country_data = open('data/country_data/Greece_data.csv', 'rt')
	csv_reader = csv.reader(country_data)
	next(csv_reader, None)

	prev_filename = ""
	cur_filename = ""

	# page_array is a 15 by 12 matrix where, same as time_array, the rows refer
	# to the years 2001 to 2015, and the columns represent each month of the
	# year. This matrix stores the average or sum of different Wikipedia
	# metrics of one particular page (e.g. Grand Duchy of Tuscany, Islam in
	# Sierra Leone)
	page_array = [[0 for num in range(12)] for num in range(2001,2016)]

	# This for loop goes through all the lines in the input file. The input
	# file is in CSV format, where the colums are:
	# filename,year,month,num_citations,file_size,forward_links,score
	# The lines are ordered by filename. As this for loop goes through the
	# file, and for all the lines with the same filename, it stores the
	# Wikipedia metrics in page_array according to their month and year.
	# If the next line read has a different filename, it will add the previous
	# information stored in page_array to the big time_array matrix, and update
	# num_array as well. Afterwards, assign 0s to the page_array.
	for line in csv_reader:
		if line[1]!='':
			cur_filename = line[0]

			# We are at a new file, so we need to update the time_array. 
			if cur_filename != prev_filename:

				# Since the input file might not have data for each month of each
				# year for each page, the page_array matrix stored so far will be
				# a sparse matrix. Thus, for all the indices where the value is 0
				# (which means that the page was not updated for that month-year
				# pair), fill it with the latest value stored (i.e. the last time
				# the page was updated).
				last_value = 0
				for year in range(2001, 2016):
					for month in range(12):
						if page_array[year-2001][month] == 0:
							page_array[year-2001][month] = last_value
						elif page_array[year-2001][month] != 0:
							last_value = page_array[year-2001][month]

				# Add the values in page_array to the big time_array.
				for year in range(2001,2016):
					for month in range(12):
						if page_array[year-2001][month]!=0:
							time_array[year-2001][month] += page_array[year-2001][month]
							num_array[year-2001][month] += 1

						# Reassign 0s to the page_array
						page_array[year-2001][month] = 0

			# Update page_array as necessary.
			page_array[int(line[1])-2001][int(line[2])-1] = int(line[5])

			# Assign the cur_filename to prev_filename
			prev_filename = cur_filename

	# Now that we've gone through the whole CSV file, get the average file size per month-year pair
	# and then write to the desired output file.
	csv_writer = csv.writer(open('data/country_data/Greece_avg_fwdlinks.csv', 'wt'))
	csv_writer.writerow(('year', 'month', 'fwd links'))

	for year in range(2001,2016):
		for month in range(12):
			if num_array[year-2001][month] != 0:
				avg = float(time_array[year-2001][month])/float(num_array[year-2001][month])
			else:
				avg = 0.0
			csv_writer.writerow((year, month, avg))