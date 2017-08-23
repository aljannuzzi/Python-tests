#!/usr/bin/python3

import configparser
from pydocumentdb import document_client

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

uri = appConfig.get("cosmos", "uri")
key = appConfig.get("cosmos", "key")

client = document_client.DocumentClient(uri, {'masterKey': key})


