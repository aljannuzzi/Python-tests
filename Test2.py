#!/usr/bin/python3

from __future__ import print_function

while True:
    reply = input('Enter text:')
    if reply == 'stop':
        break
    try:
        print(float(reply) ** 2)
    except:
        print('Bad' * 8)
print('Bye')
