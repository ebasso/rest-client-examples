# -*- coding: utf-8 -*-
#
# Necessary libraries:
#
# > pip install requests
#
# For documentation on Tone Analyzer:
#    https://watson-api-explorer.mybluemix.net/apis/tone-analyzer-v3#!/tone/GetTone
#
#
#To create an instance of the service:
#
# Log in to Bluemix.
#   1) Create an instance of the service:
#   2) In the Bluemix Catalog, select the Watson service you want to use. For example, select the Conversation service.
#   3) Type a unique name for the service instance in the Service name field. For example, type my-service-name. Leave the default values for the other options.
#   4) Click Create.
#
# To get your service credentials:
#   1) On the Service Details page,
#   2) click Service Credentials,
#   3) and then View credentials.
#   4) Copy username and password.

import sys, time, json
import requests,urllib
from requests.auth import HTTPBasicAuth

BLUEMIX_URL = 'https://gateway.watsonplatform.net/language-translator/api/v2/translate'
BLUEMIX_API_USERNAME = '<REPLACE_HERE>'
BLUEMIX_API_PASSWORD = '<REPLACE_HERE>'

def doGetTranslateWithWatson(textToTranslate, source, target):
    params = {
        'source': source,
        'target': target,
        'text':  textToTranslate
    }
    url = BLUEMIX_URL + '?'+ urllib.urlencode(params);
    headers = { 'Content-Type': 'application/json'}
    auth=HTTPBasicAuth(BLUEMIX_API_USERNAME, BLUEMIX_API_PASSWORD)

    res = requests.get(url=url,headers=headers,auth=auth)

    if (res.status_code != 200):
        print 'requests.get -> %s = %s\n' % (res.url, res)
        return None;

    return res.content


def doPostTranslateWithWatson(textToTranslate=None, source=None, target=None):
    url = BLUEMIX_URL

    headers = { 'Accept': 'application/json' }
    auth=HTTPBasicAuth(BLUEMIX_API_USERNAME, BLUEMIX_API_PASSWORD)

    #if model_id is None and (source is None or target is None):
    data = { 'text': textToTranslate, 'source': source, 'target': target}

    res =  requests.post(url=url, auth=auth, json=data)

    if (res.status_code != 200):
        print 'requests.post -> %s = %s\n' % (res.url, res)
        print res.content
        return None;

    return res.content


#################### Main Module ###################
print 'Connecting to Bluemix...\n'


textToTranslate = """
Bom dia a todos!
"""
# Portugues->English
print '----- Translate from Portuguese to English (POST):\n'
print 'Source: ', textToTranslate
print 'Target: '
print doPostTranslateWithWatson(textToTranslate, 'pt', 'en')
print '--------------------------------------------------------\n'

textToTranslate = """
Bom dia a todos!
"""
# Portugues->English
print '----- Translate from Portuguese to English (GET):\n'
print 'Source: ', textToTranslate
print 'Target: '
print doGetTranslateWithWatson(textToTranslate, 'pt', 'en')
print '--------------------------------------------------------\n'


textToTranslate = """
Bom dia a todos!
"""

print '----- Translate from Portuguese to Espanhol:\n'
outputEnglish = doGetTranslateWithWatson(textToTranslate, 'pt', 'en')
print 'Source: ', textToTranslate
print 'Target: '
print doGetTranslateWithWatson(outputEnglish, 'en', 'es')
print '--------------------------------------------------------\n'
