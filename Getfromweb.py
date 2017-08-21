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
         print(item)
         Songs[item] = []
         for musics_raw in item.next_elements:
            print (musics_raw)
#           musics_raw1 = re.sub(r".*br.*$", "", str(musics_raw))
#           musics_raw2 = re.sub(r".*INCLUD.*", "", str(musics_raw1))
#           musics_raw3 = re.sub(r".*<.*", "", str(musics_raw2))
#           musics_raw4 = re.sub(r"^$", "", str(musics_raw3))
#           musics_raw5 = re.sub(r"\n", "", musics_raw4)
#           musics_raw6 = re.sub(r"Editable", "", musics_raw5)
          
#           if musics_raw6:
#                 print (musics_raw6)
#                 Songs[item].append(musics_raw6)
       i=i+1
           
#    print (Songs)   

else:
    print ('Deu errado')
