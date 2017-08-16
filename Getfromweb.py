#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.beatlesinterviews.org/index2.html')
page_soup = BeautifulSoup(page.content, 'html.parser')

if page.status_code == requests.codes.ok:
    print ('Deu certo')
    print (page.text)
else:
    print ('Deu errado')
