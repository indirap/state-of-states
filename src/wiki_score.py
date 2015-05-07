"""
wiki_score.py
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

	MONTHS = [num+1 for num in range(12)]
	YEARS = [num for num in range(2001,2016)]

	time_array = [[0 for num in range(12)] for num in range(2001,2016)]
	num_array = [[0 for num in range(12)] for num in range(2001,2016)]
4
	country_data = open('data/country_data/Greece_data.csv', 'rt')
	csv_reader = csv.reader(country_data)
	next(csv_reader, None)

	# filename,year,month,num_citations,file_size,forward_links,score

	prev_filename = ""
	cur_filename = ""
	page_array = [[0 for num in range(12)] for num in range(2001,2016)]

	for line in csv_reader:
		if line[1]!='':
			cur_filename = line[0]
			if cur_filename != prev_filename:
				# Need to add the file sizes of this current page (page_array) to
				# the big matrix (time_array)

				# Fill the empty parts of page_array with the latest values
				last_value = 0
				for year in range(2001, 2016):
					for month in range(12):
						if page_array[year-2001][month] == 0:
							page_array[year-2001][month] = last_value
						elif page_array[year-2001][month] != 0:
							last_value = page_array[year-2001][month]

				# print the values in the page_array
				print("#### ####")
				for year in range(2001,2016):
					for month in range(12):
						print(str(year) + "-" + str(month) + " " + str(page_array[year-2001][month]))

				# Add the values in page_array to the big time_array
				for year in range(2001,2016):
					for month in range(12):
						if page_array[year-2001][month]!=0:
							print("BEFORE: " + str(time_array[year-2001][month]) + " vs. " + str(page_array[year-2001][month]))
							time_array[year-2001][month] += page_array[year-2001][month]
							print("AFTER: " + str(time_array[year-2001][month]) + " vs. " + str(page_array[year-2001][month]))
							num_array[year-2001][month] += 1

						# Reassign 0s to the page_array
						page_array[year-2001][month] = 0

				# print the values in time_array
				print("@@@@ @@@@")
				for year in range(2001,2016):
				 	for month in range(12):
				 		print(str(year) + "-" + str(month) + " " + str(time_array[year-2001][month]))
			
			# Assign the value to page_array
			print(line[1] + " " + line[2] + " - " + line[5])
			page_array[int(line[1])-2001][int(line[2])-1] = int(line[5])

			# Assign the cur_filename to prev_filename
			prev_filename = cur_filename

	# Now that we've gone through the whole csv file, get the average file size per month-year pair,
	# and then write to disk?
	csv_writer = csv.writer(open('data/country_data/Greece_avg_fwdlinks.csv', 'wt'))
	csv_writer.writerow(('year', 'month', 'fwd links'))

	print("<><><><><><><><><><><><><><><><><><><><><><><><><><><>")
	for year in range(2001,2016):
		for month in range(12):
			if num_array[year-2001][month] != 0:
				avg = float(time_array[year-2001][month])/float(num_array[year-2001][month])
			else:
				avg = 0.0
			# avg = time_array[year-2001][month]
			print(str(year) + " " + str(month) + " - " + str(avg))
			csv_writer.writerow((year, month, avg))