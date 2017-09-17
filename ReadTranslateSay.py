#!/usr/bin/python3.6

import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import configparser
import sys
from xml.etree import ElementTree

appConfig = configparser.ConfigParser()
appConfig.read("out/settings.ini")

subscription_key = appConfig.get("vision", "key")
subscription_key_speech = appConfig.get("speech", "key")

uri_base = 'westus.api.cognitive.microsoft.com'

def ReadTextFromImage(URLImagePath):
    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
    }   

    params = urllib.parse.urlencode({
    # Request parameters. The language setting "unk" means automatically detect the language.
    'language': 'unk',
    'detectOrientation ': 'true',
    })

    body = "{'url':'" + URLImagePath + "'}"

    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        
        D = eval(str(json.dumps(parsed, sort_keys=True, indent=2)))
        
        textout = ""

        for a in (range(len(D["regions"]))):
            for i in (range(len(D["regions"][a]["lines"]))):
                for j in range(len(D["regions"][a]["lines"][i]["words"])):
                    # print ((D["regions"][0]["lines"][i]["words"][j]["text"]), end=' ')
                        textout = textout + " " + D["regions"][a]["lines"][i]["words"][j]["text"]

        conn.close()

        return textout

    except Exception as e:
        print('Error:')
        print(e)
        return False

def GetAudioFromText(text2narrate, audiofileoutput):
    params_speech = ""
    headers_speech = {"Ocp-Apim-Subscription-Key": subscription_key_speech}

    AccessTokenHost = "api.cognitive.microsoft.com"
    path = "/sts/v1.0/issueToken"

    try:
        # Connect to server to get the Access Token
        conn = http.client.HTTPSConnection(AccessTokenHost)
        conn.request("POST", path, params_speech, headers_speech)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        accesstoken = data.decode("UTF-8")

        # Compose body and set the text2speech
        body = ElementTree.Element('speak', version='1.0')
        body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
        voice.text = text2narrate

        # Set the headers

        headers = {"Content-type": "application/ssml+xml", 
		            "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm", 
                    "Authorization": "Bearer " + accesstoken, 
                    "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA", 
                    "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960", 
                    "User-Agent": "TTSForPython"}

        #Connect to server to synthesize the wave

        conn = http.client.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        # Write audio to file

        outfile = open(audiofileoutput, 'wb')
        outfile.write(data)

        return 1
    
    except Exception as e:
        print('Error:')
        print(e)

        return False


# Begining of the main body. Uhmm, missing main() :-)

text2read = ReadTextFromImage('http://www.funpedia.net/imgs/may11/very-funny-signs-01.jpg')
print (text2read)

if text2read:
    GetAudioFromText(text2read, 'saida.audio')

