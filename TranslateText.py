#!/usr/bin/python3.6

import requests
import configparser
from xml.etree import ElementTree

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

subscription_key = appConfig.get("translation", "key")

request_headers = {'Ocp-Apim-Subscription-Key': subscription_key}

textToTranslate = 'This is the first test'

translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}".format(textToTranslate, 'pt')

translationData = requests.get(translateUrl, headers = request_headers)

translation = ElementTree.fromstring(translationData.text.encode('utf-8'))

print (translation.text)

