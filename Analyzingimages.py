#!/usr/bin/python3.6

import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import configparser
import sys

try:
    imagepath = sys.argv[1]
    print (imagepath)

except:
    print("Usage:" + sys.argv[0] + " <URL of image to analyze")
#    sys.exit("Terminating due to lack of required parameters")

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

subscription_key = appConfig.get("vision", "key")

uri_base = 'westus.api.cognitive.microsoft.com'

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})


body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'}"
#body = "{'url':'" + imagepath + "'}"

try:
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)
