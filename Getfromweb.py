#!/usr/bin/python3

import requests


page = requests.get('http://www.beatlesinterviews.org/index2.html')

if page.status_code == requests.codes.ok:
    print ('Deu certo')
    print (page.text)
else:
    print ('Deu errado')
