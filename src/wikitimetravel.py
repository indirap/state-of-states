'''
wikitimetravel.py
'''
import urllib2
from datetime import date
from bs4 import BeautifulSoup

def make_edit_list_url(title,limit,offset):
    return 'https://en.wikipedia.org/w/index.php?title='+title+'&action=history&limit='+str(limit)+'&offset='+str(offset)

def obtain_date(edit):
    conversion = {"January":1,
                  "February":2,
                  "March":3,
                  "April":4,
                  "May":5,
                  "June":6,
                  "July":7,
                  "August":8,
                  "September":9,
                  "October":10,
                  "November":11,
                  "December":12}
    text_date = edit.string.split(",")[1]
    comp = text_date.strip().split(" ")
    return date(int(comp[2]), conversion[comp[1]], int(comp[0]))

def obtain_url(edit):
    stem = 'https://en.wikipedia.org'
    return stem+edit['href']

def obtain_edits(soup):
    '''
    Given a soup, returns a list of tuples of date and url
    '''
    results = [] # List of tuples
    edits = soup.find_all(id="pagehistory")[0].find_all("a", class_="mw-changeslist-date")
    for edit in edits:
        results.append((obtain_date(edit), obtain_url(edit)))
    return results

def check_date(candidate_date, prev_date):
    if prev_date == None:
        return True
    sameyear = (candidate_date.year == prev_date.year and candidate_date.month < prev_date.month)
    prevyear = (candidate_date.year < prev_date.year)
    return sameyear or prevyear

def edit_pages(title):
    limit = 100
    offset = ""
    url = make_edit_list_url(title, limit, offset)
    while True:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read())
        page.close()
        for edit in obtain_edits(soup):
            yield edit
        if len(soup.find_all("a",class_="mw-nextlink")) == 0:
            print url
            return
        else:
            url = 'https://en.wikipedia.org' + soup.find_all("a", class_="mw-nextlink")[0]['href']
    return

#Generator
def wiki_history_by_month(title, start_date):
    #edit_list_url = make_edit_list_url(title,limit,offset)
    last_returned_date = None
    gen = edit_pages(title)
    while True:
        (page_date, edit_url) = next(gen)
        if page_date >= start_date:
            if check_date(page_date, last_returned_date):
                last_returned_date = page_date
                yield (page_date, edit_url)
        else:
            return

if __name__=="__main__":
    start_date = date(2008, 12,1)
    for page in wiki_history_by_month("Bahrain",start_date):
        print str(page[0]) + "\t" + page[1]
