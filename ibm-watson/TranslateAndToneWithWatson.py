#!/usr/local/bin/python2.7
# encoding: utf-8
import sys, time, json
import requests,urllib
from requests.auth import HTTPBasicAuth

class LanguageTranslator:

    def __init__(self,BLUEMIX_API_USERNAME=None,BLUEMIX_API_PASSWORD=None):
        self.BLUEMIX_URL = 'https://gateway.watsonplatform.net/language-translator/api/v2/translate'
        self.BLUEMIX_API_USERNAME = BLUEMIX_API_USERNAME
        self.BLUEMIX_API_PASSWORD = BLUEMIX_API_PASSWORD

    #def postTranslate(self,textToTranslate=None, source=None, target=None):
    def translate(self,textToTranslate=None, source=None, target=None):
        url = self.BLUEMIX_URL

        headers = { 'Accept': 'application/json' }
        auth=HTTPBasicAuth(self.BLUEMIX_API_USERNAME, self.BLUEMIX_API_PASSWORD)

        #if model_id is None and (source is None or target is None):
        data = { 'text': textToTranslate, 'source': source, 'target': target}

        res =  requests.post(url=url, auth=auth, json=data)

        if (res.status_code != 200):
            print 'requests.post -> %s = %s\n' % (res.url, res)
            print res.content
            return None;

        if (res.headers['Content-Type'] != 'text/plain;charset=utf-8'):
            print res.headers['Content-Type']

        return res.content

class ToneAnalyzer:

    def __init__(self,BLUEMIX_API_USERNAME=None,BLUEMIX_API_PASSWORD=None):
        self.BLUEMIX_URL = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone'
        self.BLUEMIX_API_USERNAME = BLUEMIX_API_USERNAME
        self.BLUEMIX_API_PASSWORD = BLUEMIX_API_PASSWORD

    def tone(self,textToAnalyze):

        data = {
                'text':  textToAnalyze
        }
        params = {
            'version': '2016-05-19'
        }
        url = self.BLUEMIX_URL + '?'+ urllib.urlencode(params);
        headers = { 'Accept': 'application/json'}
        auth=HTTPBasicAuth(self.BLUEMIX_API_USERNAME, self.BLUEMIX_API_PASSWORD)

        res = requests.post(url=url,headers=headers,auth=auth,json=data)
        if (res.status_code != 200):
            print 'doGetToneAnalyze: requests.post -> %s = %s\n' % (res.url, res)
            print res.content
            return None;

        if (res.headers['Content-Type'] != 'application/json'):
            print 'doGetToneAnalyze: No Json returned'
            return None

        return res.json()



#################### Main Module ###################
print 'Connecting to Bluemix...\n'

print '############ Translate from Portuguese to English (POST) #############\n'
translator = LanguageTranslator('<REPLACE_HERE_USERNAME>','<REPLACE_HERE_PASSWORD>')

textToTranslate = """
Bom dia a todos!
"""

print 'Source: ', textToTranslate
print 'Target: '
outputEnglish = translator.translate(textToTranslate, 'pt', 'en')
if (outputEnglish is None):
    print 'Cannot get Translate.'
    sys.exit(1)

print outputEnglish
print '----------------------------------------------------------------------\n'



print '######################## Tone Analyzer (POST) ########################\n'
ta = ToneAnalyzer('<REPLACE_HERE_USERNAME>','<REPLACE_HERE_PASSWORD>')

print 'Text to Analyze:\n'
print outputEnglish

print 'Start Tone Analyzer:\n'
output = ta.tone(outputEnglish)
if (output is None):
    print 'Cannot get Tone Analyze.'
    sys.exit(1)

print 'List Tone Analyzer\n'
document_tone = output['document_tone']
tone_categories = document_tone['tone_categories']
for category in tone_categories:
    print ' ' + category['category_name']
    print ' |--> category_id: ' + category['category_id']
    print ' |--> tones: (tone_name,tone_id,score)'
    for tone in category['tones']:
        print ' |----> (%s, %s, %s)' % (tone['tone_name'], tone['tone_id'], tone['score'])
    print
print '----------------------------------------------------------------------\n'
