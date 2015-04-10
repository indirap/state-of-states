from bs4 import BeautifulSoup
import sys

# Usage
# First argument is the html file (in the data folder)
# Second argument is the output file for a list of country urls
# Third argument is the output file for a list of category urls

soup = BeautifulSoup(open(sys.argv[1]))
name_out = open(sys.argv[2], 'w+')
cats_out = open(sys.argv[3], 'w+')

#Finds the rows of the table
names = soup.find_all("td", style="vertical-align:top;")


#The part of the url not 
forward = 'http://wikipedia.org'

#For each row in the table
for name in names:
    link = name.find_all('a')[0]
    if '/wiki/' in link['href']:
        name_out.write(forward + link['href'] + '\n')
        cats_out.write(forward + link['href'][:6] + 'Category:' + link['href'][6:] + '\n')

name_out.close()
cats_out.close()

