# -*- coding: utf-8 -*-
#
# Necessary libraries:
#
# > pip install requests
#
# For documentation on Tone Analyzer:
#    https://watson-api-explorer.mybluemix.net/apis/tone-analyzer-v3#!/tone/GetTone
#
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CONNECTIONS_HOST = 'https://connections.<company>.com'
CONNECTIONS_USERNAME = '<REPLACE_HERE>'
CONNECTIONS_PASSWORD = '<REPLACE_HERE>'

wiki_id_or_label = 'W34c618febb3c_4a55_81b7_0d5a81dc1954';

xml_data = ''
xml_data += '<entry xmlns="http://www.w3.org/2005/Atom">'
xml_data += '<title type="text">My First Wiki Python</title>'
xml_data += '<content type="text/html">'
xml_data += '<![CDATA[<?xml version="1.0" encoding="UTF-8"?><p>'
xml_data += '<strong>Hello World!</strong>'
xml_data += '</p>]]>'
xml_data += '</content>'
xml_data += '<category term="wikipagetag1" />'
xml_data += '<category term="wikipagetag2" />'
xml_data += 'category scheme="tag:ibm.com,2006:td/type" term="page" label="page" />'
xml_data += '</entry>'

xml_data2 = '''
<entry xmlns="http://www.w3.org/2005/Atom">
<title type="text">My First Wiki Python 2</title>
<content type="text/html">
<![CDATA[<?xml version="1.0" encoding="UTF-8"?><p>
<strong>Hello World!</strong>
</p>]]>
</content>
<category term="wikipagetag1" />
<category term="wikipagetag2" />
category scheme="tag:ibm.com,2006:td/type" term="page" label="page" />
</entry>
'''

def createWikiPage(wiki_id_or_label, xml_data):

    headers = { 'Content-Type': 'application/atom+xml;charset=UTF-8'}

    url = CONNECTIONS_HOST + '/wikis/basic/api/wiki/' + wiki_id_or_label  + '/feed'
    auth=HTTPBasicAuth(CONNECTIONS_USERNAME, CONNECTIONS_PASSWORD)

    res = requests.post(url=url,headers=headers,auth=auth,verify=False,data=xml_data)
    if (res.status_code != 200):
        print 'doGetToneAnalyze: requests.post -> %s = %s\n' % (res.url, res)
        print res.content
        return None;

    return res.json()

#################### Main Module ###################
print 'Connecting to IBM Connections...\n'

print 'Creating Wiki Page...\n'
createWikiPage(wiki_id_or_label,xml_data)
createWikiPage(wiki_id_or_label,xml_data2)
