import requests
import sys
from bs4 import BeautifulSoup

EMAIL = 'donalddbest'
PASSWORD = '667432aa'

URL = 'https://www.morphmarket.com/us/c/reptiles/pythons/ball-pythons/79400'

def main():
    # Start a session so we can have persistant cookies
    session = requests.session()

    # This is the form data that the page sends when logging in
    login_data = {
        'login': EMAIL,
        'loginpswd': PASSWORD,
        'submit': 'login',
    }

    # Authenticate
    r = session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in
    r = session.get('https://www.morphmarket.com/us/c/reptiles/pythons/ball-pythons/79400')
    bs = BeautifulSoup(r.content)
    price = bs.find("meta",{"name":"description"})
    traitsfile = open('traitsfile.txt','w')
    traitsfile.write("%s" % bs)

if __name__ == '__main__':
    main()