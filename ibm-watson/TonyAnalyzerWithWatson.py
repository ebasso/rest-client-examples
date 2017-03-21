# -*- coding: utf-8 -*-
#
# Necessary libraries:
#
# > pip install requests
#
# For documentation on Tone Analyzer:
#    https://watson-api-explorer.mybluemix.net/apis/tone-analyzer-v3#!/tone/GetTone
#
import sys, time, json
import requests,urllib
from requests.auth import HTTPBasicAuth

BLUEMIX_URL = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone'
BLUEMIX_API_USERNAME = '<REPLACE_HERE>'
BLUEMIX_API_PASSWORD = '<REPLACE_HERE>'


def doGetToneAnalyze(textToAnalyze):

    params = {
        'version': '2016-05-19',
        'text':  textToAnalyze
    }
    url = BLUEMIX_URL + '?'+ urllib.urlencode(params);
    print url + '\n'

    headers = { 'Accept': 'application/json'}
    auth=HTTPBasicAuth(BLUEMIX_API_USERNAME, BLUEMIX_API_PASSWORD)

    res = requests.get(url=url,headers=headers,auth=auth)
    if (res.status_code != 200):
        print 'doGetToneAnalyze: requests.get -> %s = %s\n' % (res.url, res)
        print res.content
        return None;

    if (res.headers['Content-Type'] != 'application/json'):
        print 'doGetToneAnalyze: No Json returned'
        return None

    return res.json()

def doPostToneAnalyze(textToAnalyze):

    data = {
            'text':  textToAnalyze
    }
    params = {
        'version': '2016-05-19'
    }
    url = BLUEMIX_URL + '?'+ urllib.urlencode(params);
    headers = { 'Accept': 'application/json'}
    auth=HTTPBasicAuth(BLUEMIX_API_USERNAME, BLUEMIX_API_PASSWORD)

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

textToAnalyze = """
What happens with Logan?
"""

print 'Text to Analyze:\n'
print textToAnalyze

print 'Start Tone Analyzer:\n'
#output = doGetToneAnalyze(textToAnalyze)
output = doPostToneAnalyze(textToAnalyze)

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
print '--------------------------------------------------------\n'
