'''
category_downloader.py
Purpose:
    Takes in a file of category urls. For each url it will recursively search through
    all the pages associated with the category/subcategories. These will be saved into
    a folder indicated by output.
    The output will be organized by the original category in a flat system.
    
TODO: Support multiple versions with user defined increments. For now this will
just download the current pages
'''
import sys
import os
import urllib2
from datetime import date
from bs4 import BeautifulSoup
from wikitimetravel import wiki_history_by_month

url_stem = 'https://en.wikipedia.org'
visited_categories = set()

def download_page(url,output_filename):
    '''
    Downloads a page to a given location
    '''
    response = urllib2.urlopen(url)
    html = response.read()
    out_file = open(output_filename, 'w+')
    out_file.write(html)
    out_file.close()

def check_category(country, url, depth):
    if country in get_category_name(url) or depth < 4:
        return True
    return False


def obtain_subcategory_urls(soup):
    '''
    Given a soup, returns a list of urls
    '''
    sub_cats = soup.find_all("a", class_="CategoryTreeLabel")
    return [url_stem + cat['href'] for cat in sub_cats]

def obtain_page_urls(soup):
    '''
    Given a soup, returns a list of urls
    '''
    if len(soup.find_all(id="mw-pages")) != 0:
        links = soup.find_all(id="mw-pages")[0].find_all(class_="mw-content-ltr")[0].find_all("a")
        return [url_stem + link['href'] for link in links]
    else:
        return []

def get_subcategories_and_pages(url):
    '''
    Given a url, returns a tuple of
        list of subcategory urls
        list of page urls
    '''
    assert('Category' in url)
    #Start Up
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    #Find the stuff
    subcategory_urls = obtain_subcategory_urls(soup)
    page_urls = obtain_page_urls(soup)
    #Finish Up
    page.close()
    return (subcategory_urls, page_urls)



def download_category(country, url, output_location, depth):
    '''
    Recursively downloads pages in categories and subcategories
    '''
    #Reasons for stopping
    if url in visited_categories or not check_category(country, url, depth):
        return

    visited_categories.add(url)
    page_data = get_subcategories_and_pages(url)
    for i in xrange(depth): sys.stdout.write(".")
    print url
    subcategories = page_data[0]
    pages = page_data[1]
    for subcat in subcategories: download_category(country, subcat, output_location, depth+1)
    for page in pages:
        for vdate, vurl in wiki_history_by_month(get_page_name(page),date(2000,12,1)):
            download_page(vurl, create_file_name(page, vdate.isoformat(), output_location))


def create_file_name(url, date_string, output_location):
    '''
    pagename-YYYY-MM-DD.html
    '''
    return output_location + "/" + "-".join([get_page_name(url), date_string]) + ".html"


def get_category_name(url):
    return url[35:].strip()

def get_page_name(url):
    return url[30:].strip()

if __name__ == "__main__":
    category_urls = sys.argv[1]
    output_location = sys.argv[2]
    with open(category_urls) as f:
        for url in f:
            visited_categories = set()
            print get_category_name(url)

            #Create dir for each country
            new_output_location = output_location+"/"+get_category_name(url)
            if not os.path.exists(new_output_location):
                os.makedirs(new_output_location)

            download_category(get_category_name(url), url, new_output_location, 0)
    print "Done"
