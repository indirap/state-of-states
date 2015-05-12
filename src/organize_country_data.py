'''
Not used, see wiki_score.py
'''
import os
import csv
import sys


def gen_date(start_date, end_date):
    cur_date = [start_date[0], start_date[1]]
    while cur_date[0] < end_date[0]:
        while cur_date[1] <= 11:
            cur_date[1] = cur_date[1] + 1
            yield (cur_date[0], cur_date[1])
        cur_date[0] = cur_date[0] + 1
        cur_date[1] = 1
    #Here then the year is the same
    while cur_date[1] <= end_date[1]:
        cur_date[1] = cur_date[1] + 1
        yield (cur_date[0], cur_date[1])

def write_formatted_country(country_fd, data):
    # Start at: 2001-07
    # End at: 2015-04
    date_keys = ["".join([str(d[0]),"-","%02d" % d[1]]) for d in gen_date((2001,7),(2015,04))]
    print date_keys

    writer = csv.writer(country_fd)
    writer.writerow(['filename','feature'] + date_keys)

    for filename in data.keys():
        print str(len(data[filename])) +"\t" + filename
        writer.writerow([filename, 'num_citations'] + [data[filename][date_key][0] if date_key in data[filename] else -1 for date_key in date_keys])
        #writer.writerow([filename, 'file_size'] + [data[filename][date_key][1] if date_key in data[filename] else -1 for date_key in date_keys])
        #writer.writerow([filename, 'forward_links'] + [data[filename][date_key][2] if date_key in data[filename] else -1 for date_key in date_keys])

def format_country_data(country_fd):
    #Data: page:{(year-months): (num_citations,file_size,forward_links)}
    data = {}
    reader = csv.DictReader(country_fd)
    for row in reader:
        if not row['filename'] in data:
            data[row['filename']] = {}
        date_key = "".join([row['year'],"-", row['month']]) 
        #date_key = (row['year'], row['month'])
        #print row['filename']
        #print date_key
        #assert(not date_key in data[row['filename']])
        data[row['filename']][date_key] = (row['num_citations'],row['file_size'],row['forward_links'])
    return data

def format_all_countries(input_dir, output_dir):
    country_files = [ f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir,f))]
    for country_file in country_files:
        #Read and format
        print os.path.join(input_dir, country_file)
        country_fd = open(os.path.join(input_dir, country_file), "r")
        res = format_country_data(country_fd)
        country_fd.close()
        #Write
        formatted_country_fd = open(os.path.join(output_dir,country_file), "w+")
        write_formatted_country(formatted_country_fd, res)
        formatted_country_fd.close()


if __name__ == "__main__":
    #Locations
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    #Check some things
    if not os.path.exists(input_dir):
        print "Input directory does not exist"
        sys.exit(0)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    #Format all the countries
    format_all_countries(input_dir, output_dir)

