import random
from os import listdir
from os.path import join, basename
from itertools import combinations
import sys
import csv
import scipy.stats
from sklearn import cross_validation
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet
import numpy as np

# Takes a joined data set and calculates pearson correlation on data
def calc_pearson_correlation(filename):
    # Load data
    gdp_data = []
    citation_data = []
    fsize_data = []
    link_data = []


    fd = open(filename, 'r')
    reader = csv.reader(fd, delimiter='\t')

    reader.next()

    for line in reader:
        if line[3] =="":
            continue
        gdp_data.append(float(line[3]))
        citation_data.append(int(line[4]))
        fsize_data.append(int(line[5]))
        link_data.append(int(line[6]))

    #Correlate
    print sys.argv[1] + "\tCitation\t" + str(scipy.stats.pearsonr(gdp_data, citation_data)[0])
    print sys.argv[1] + "\tFile Size\t" + str(scipy.stats.pearsonr(gdp_data, fsize_data)[0])
    print sys.argv[1] + "\tLinks\t" + str(scipy.stats.pearsonr(gdp_data, link_data)[0])


# Takes a list of files and calculates the linear regression
# Taking in the WB features to predict each of the Wiki features
# For now we're just looking at citations
# May be a problem with 0 values here, let's see
def calc_linear_regression(files, data_matrix, target, results):

    lr = Lasso()
    lr.fit(data_matrix, target)

    rss = np.mean((lr.predict(data_matrix) - target) ** 2)
    var = lr.score(data_matrix, target)

    global best
    if rss < best:
        for i in range(0,len(target)):
            print str(target[i]) + "\t" + str(lr.predict(data_matrix[i])[0])
        print lr.coef_
        best = rss

    results.append((files, rss, var, lr.coef_))

def get_indicator_values(file_name):
    data = []
    reader = csv.reader(open(file_name, 'r'), delimiter="\t")
    reader.next()
    for i,line in enumerate(reader): # For country in file
        if line[3] == "":
            data.append(0.0)
        else:
            data.append(float(line[3]))
    return data

def get_wiki_values(file_name):
    '''Takes a filename and returns a list of (citations, fsize, links)'''
    data = []
    reader = csv.reader(open(file_name, 'r'), delimiter="\t")
    reader.next()
    for i,line in enumerate(reader): # For country in file
        data.append((float(line[4]), float(line[5]), float(line[6])))
    return data

def get_file_names(dir_path):
    return [ join(dir_path,f) for f in listdir(dir_path) ]

if __name__ == "__main__":
    if len(sys.argv) == 0:
        print " Invalid options"
    if sys.argv[1] == 'pearson-correlation':
        calc_pearson_correlation(sys.argv[2])
    elif sys.argv[1] == 'linear-regression': 
        #Try combinations of linear regression, next args: num, dir
        results = []
        file_names = get_file_names(sys.argv[3])
        indicator_values = {}
        wiki_values = get_wiki_values(file_names[0])

        #Cache the indicator data
        for f in file_names:
            indicator_values[f] = get_indicator_values(f)

        for files in combinations(file_names, int(sys.argv[2])):
        #for files in [random.sample(file_names, int(sys.argv[2]))]:
            print len(results)
            best = float("inf")
            calc_linear_regression(
                files,
                np.array([indicator_values[f] for f in files]).transpose(),
                np.array([w[0] for w in  wiki_values]),
                results) # list of files

        results.sort(key=lambda result: result[1])

        #Print out the best
        for i, res in enumerate(results):
            if i >5:
                break;
            print str([basename(f) for f in res[0]]) + ": " +str(res[1])
    elif sys.argv[1] == 'custom':
        #This option to specify exactly which to use
        files = sys.argv[2:]
        indicator_values = {}
        results = []
        best = 0
        wiki_values = get_wiki_values(files[0])
        #Cache the indicator data
        for f in files:
            indicator_values[f] = get_indicator_values(f)
        calc_linear_regression(
            files,
            np.array([indicator_values[f] for f in files]).transpose(),
            np.array([w[0] for w in wiki_values]),
            results) # list of files
