#!/usr/bin/python3.6

import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import configparser
import sys

try:
    imagepath = sys.argv[1]
    print (imagepath)

except:
    print("Usage:" + sys.argv[0] + " <URL of image to analyze")
    sys.exit("Terminating due to lack of required parameters")

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

subscription_key = appConfig.get("vision", "key")

uri_base = 'westus.api.cognitive.microsoft.com'

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
})

# The URL of a JPEG image containing text.
#body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"

body = "{'url':'" + imagepath + "'}"

try:
    # Execute the REST API call and get the response.
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print('Error:')
    print(e)

####################################