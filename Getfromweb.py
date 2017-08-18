#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re
Songs = {}

page = requests.get('http://www.beatlesinterviews.org/index2.html')

if page.status_code == requests.codes.ok:
  #  print (page.text)
    page_soup = BeautifulSoup(page.content, 'html.parser')

    #print (page_soup.contents)
    i=0
    for item in page_soup.find_all(text=re.compile("^[A-Z]{3,100}")):
       if i > 1:
         for musics in item.next_elements:
           print (musics)
         Songs[item]={}
       i=i+1

else:
    print ('Deu errado')
