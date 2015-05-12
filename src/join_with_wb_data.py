'''
join_with_wb_data.py

Combines
* datascraped from wikipedia
* data obtained from the world bank
* country codes used for the d3 map.

Takes as input
1: World Bank CSV
2: Feature TSV file from Wikipedia
3: ISO file from D3 Map

'''
import os
import csv
import sys
import os
from types import *


def clean_filename(name):
    '''Given a filename ending with .csv, returns the basename minus .csv'''
    name = os.path.splitext(name)[0]
    name = name.replace("_"," ")
    name = name.replace("data","")
    return name



def transform_name(name):
    '''
    Called on all 'name' values in all data sets,
    transforms the value into a standardized one,
    not found in any one of the datsets
    '''
    if name.endswith(".csv"):
        name = clean_filename(name)
    #Sub in countries
    if name == "Kyrgyz Republic":
        name = "Kyrgyzstan"
    elif name == "Congo, Dem. Rep.":
        name = "Democratic Republic of the Congo"
    elif name == "Congo, Rep.":
        name = "Republic of the Congo"
    elif name == "Russian Federation":
        name = "Russia"
    elif name == "Myanmar":
        name = "Burma"
    elif name == "Kingdom of the Netherlands":
        name = "Netherlands"
    elif name == "Iran, Islamic Rep.":
        name = "Iran"
    elif name == "Syrian Arab Republic":
        name = "Syria"
    elif name == "Yemen, Rep.":
        name = "Yemen"
    elif name == "Egypt, Arab Rep.":
        name = "Egypt"
    elif name =="Lao PDR":
        name = "Laos"
    elif name =="Republic of Ireland":
        name = "Ireland"
    elif name =="Venezuela, RB":
        name = "Venezuela"
    elif 'Bahamas' in name:
        name = 'Bahamas'
    elif name == 'Cabo Verde':
        name = 'Cape Verde'
    elif 'Brunei' in name:
        name = 'Brunei'
    elif name == 'Timor-Leste':
        name = 'East Timor'
    elif 'Micronesia' in name:
        name = 'Micronesia'
    elif 'Georgia' in name:
        name = 'Georgia'
    elif name == "Cote d'Ivoire":
        name = 'Ivory Coast'
    elif 'Kosovo' in name:
        name = 'Kosovo'
    elif name == 'Korea, Dem. Rep.':
        name = 'North Korea'
    elif 'Ireland' in name:
        name = 'Ireland'
    elif name == 'Macedonia, FYR':
        name = 'Macedonia'
    elif name == 'S%C3%A3o Tom%C3%A9 and Pr%C3%ADncipe':
        name = 'Sao Tome and Principe'
    elif 'Kitts and Nevis' in name:
        name = 'Saint Kitts and Nevis'
    elif name == 'St. Lucia':
        name = 'Saint Lucia'
    elif name == 'St. Vincent and the Grenadines':
        name = 'Saint Vincent and the Grenadines'
    elif name == 'Slovak Republic':
        name = 'Slovakia'
    elif name == 'Korea, Rep.':
        name = 'South Korea'
    elif 'Gambia' in name:
        name = 'Gambia'
    return name.strip().lower() #an important part


#Open files
#ISO file
iso_file = open(sys.argv[3],'r')
iso_reader = csv.reader(iso_file, delimiter='\t')
iso_reader.next()
iso_dict = {}
#Read iso file into dict: {transformed_name: (id, code)
for line in iso_reader:
    iso_dict[transform_name(line[2])] = (line[0], line[1])

#Feature file
feature_file = open(sys.argv[2],'r')
feature_reader = csv.reader(feature_file, delimiter='\t')
feature_dict = {}
#Read data into dictionary
for country in feature_reader:
    feature_dict[transform_name(country[0])] = country[1:]

#World Bank File
wb_file = open(sys.argv[1],'r')
reader = csv.reader(wb_file)
reader.next()

indicators = set() # Set of all indicators found so far

data = {}
# Get all data in form:
#   {country_code: { country_indicator: rest_of_line }}

for line in reader: #for line in world bank data set
    c_code = transform_name(line[0]) #Get country code
    c_indicator = line[3]
    indicators |= set([c_indicator]) #Add to indicator set
    if not c_code in data:
        data[c_code] = {}
    data[c_code][c_indicator] = line

field = 58 # Per WB data file, but the column for 2013

prefix = "" #Per WB data file, just for ease of identifying output

for ind in indicators: # for each indicator
    # Keeps track of num of countries with missing WB data
    # If this number goes over 50 then ignore this indicator
    num_empty = 0 
    for country_key in data.keys(): # For each country
        country = data[country_key]
        assert type(country) is DictType
        #If no indicator for this country
        if not ind in country:
            num_empty +=1 #No data, increase counter, continue
            continue
        if country[ind][field] == "":
            num_empty +=1 #Or if value is empty 
            continue
    if num_empty < 50:
        #Create output file
        fd = open("res_"+prefix+"_"+ind+".tsv", 'w+')
        writer = csv.writer(fd, delimiter='\t')
        # Write header
        writer.writerow(['id', 'code', 'country', 'indicator', 'citations', 'fsize', 'links'])
        for country_key in data.keys(): #Write out each country
            country = data[country_key]
            tname = transform_name(country[ind][0])
            if (not tname in feature_dict) or (not tname in iso_dict):
                continue
            #print iso_dict[tname][0]
            #print iso_dict[tname][1]
            #print country[ind][field]
            writer.writerow([iso_dict[tname][0], iso_dict[tname][1], tname, country[ind][field]] + feature_dict[tname])
        fd.close()
    else:
        print "Too few countries have this indicator: %s" % ind
