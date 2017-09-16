#!/usr/bin/python3.6

import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import configparser
import sys
from xml.etree import ElementTree


try:
    imagepath = sys.argv[1]
    print (imagepath)

except:
    print("Usage:" + sys.argv[0] + " <URL of image to analyze")
 #   sys.exit("Terminating due to lack of required parameters")

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

subscription_key = appConfig.get("vision", "key")
subscription_key_speech = appConfig.get("speech", "key")

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
body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png'}"

#body = "{'url':'" + imagepath + "'}"

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

    D = eval(str(json.dumps(parsed, sort_keys=True, indent=2)))
    
    print(D["regions"][0]["lines"])

    for i in (range(len(D["regions"][0]["lines"]))):
        for j in range(len(D["regions"][0]["lines"][i]["words"])):
            print ((D["regions"][0]["lines"][i]["words"][j]["text"]))


    conn.close()

except Exception as e:
    print('Error:')
    print(e)

####################################

params_speech = ""
headers_speech = {"Ocp-Apim-Subscription-Key": subscription_key_speech}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

# Connect to server to get the Access Token
print ("Connect to server to get the Access Token")
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params_speech, headers_speech)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Access Token: " + accesstoken)

body = ElementTree.Element('speak', version='1.0')
body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
voice = ElementTree.SubElement(body, 'voice')
voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
voice.text = 'Laura, you are my beautiful princess! Hi, hi, hi... Hello!!!'

headers = {"Content-type": "application/ssml+xml", 
			"X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
			"Authorization": "Bearer " + accesstoken, 
			"X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
			"X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
			"User-Agent": "TTSForPython"}
			
#Connect to server to synthesize the wave
print ("\nConnect to server to synthesize the wave")
conn = http.client.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
print("The synthesized wave length: %d" %(len(data)))

print (data)

outfile = open('audio.bin', 'wb')
outfile.write(data)