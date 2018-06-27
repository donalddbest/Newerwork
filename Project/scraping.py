import requests 
from contextlib import closing
from bs4 import BeautifulSoup
import time
from urllib import urlopen
import sys



def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

traitsfile = open('traitsfile.txt','w')

raw_html = simple_get('https://www.morphmarket.com/us/c/reptiles/pythons/ball-pythons/index?epoch=1')
html = BeautifulSoup(raw_html,'html.parser')
divs = html.find('div',{"class":'gene-index clearfix'})
anchorlist = divs.find_all('a', href  = True)
hrefs = []
traithrefs = []
for a in anchorlist:
	hrefs.append('https://www.morphmarket.com'+str(a['href']))
# for h in hrefs:
# print hrefs[0]
# new_html = urlopen(hrefs[0])
# traithtml = BeautifulSoup(new_html,'html.parser')

# traitdivs = traithtml.find_all('div',{"class":"col-md-3 col-sm-4 col-ms-4 col-xs-6 item-col move-up"})
# traitsfile.write("%s" % traithtml)
# 	time.sleep(10)
	# traitanchorlist = traitdivs.find_all('a', href = True)
	# 
	# for b in traitanchorlist:
	# 	string = 'https://www.morphmarket.com'+str(b['href'])
	# 	traitsfile.write("%s\n" % string)
new_html = urlopen('https://www.morphmarket.com/us/c/reptiles/pythons/ball-pythons/79400')
axhtml = BeautifulSoup(new_html,'html.parser')
axdiv = axhtml.find('dt',{"class":"price"})
traitsfile.write("%s" % axhtml)
