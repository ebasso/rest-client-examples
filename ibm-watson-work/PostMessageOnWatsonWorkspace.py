    #!/usr/local/bin/python2.7
# encoding: utf-8

import sys, time, datetime, json
import requests,urllib
from requests.auth import HTTPBasicAuth

appname='PostMessageOnWatsonWorkspace.py'
WWS_APPID = '<REPLACE_HERE>'
WWS_APPSECRET = '<REPLACE_HERE>'
WWS_SPACEID = '<REPLACE_HERE>'

class Workspace:

    def __init__(self,appid=None,appsecret=None,spaceid=None):
        self.appid = appid
        self.appsecret = appsecret
        self.spaceid = spaceid
        self.token = None

    def sendTextMessage(self,text):
        data = {
          'type': 'appMessage',
          'version': 1.0,
          'annotations': [{
            'type': 'generic',
            'version': 1.0,
            'color': '#388E3C',
            'title': appname + ' --> sendTextMessage',
            'text': text
          }]
        }
        return self.sendMsg(data)

    def sendRichMessage(self,text):
        data = {
          'type': 'appMessage',
          'version': 1.0,
          'annotations': [{
            'type': 'generic',
            'version': 1.0,
            'color': '#4FC3F7',
            'title': appname + ' --> sendRichMessage at ' + str(datetime.datetime.now()),
            'text': text,
            'actor': {
              'name': 'Enio Basso',
              'avatar': '',
              'url': 'https://ebasso.net'
            }
          }]
        }
        return self.sendMsg(data)

    def doOAuth(self):

        # If already has token return token
        if (self.token is not None):
            return self.token

        url = 'https://api.watsonwork.ibm.com/oauth/token'
        auth = HTTPBasicAuth(self.appid, self.appsecret)
        payload = {"grant_type":"client_credentials"}

        res = requests.post(url=url,auth=auth, data=payload)
        if res.status_code != 200:
            print 'Could not authenticate your application'
            sys.exit(1)
        data = res.json()
        self.token =  data['access_token']
        return self.token

    def sendMsg(self,data):
        url = 'https://api.watsonwork.ibm.com/v1/spaces/' + self.spaceid + '/messages'
        token = self.doOAuth()
        headers = { 'Authorization':'Bearer %s' % token, 'Accept': 'application/json'}

        res = requests.post(url=url,headers=headers,json=data)
        if (res.status_code != 201):
            print 'sendMsg: requests.post -> %s = %s\n' % (res.url, res)
            print res.content
            return None;
        data = res.json()
        return data['id']

    def errMsg(self,err):
        if (err != 201):
            print '201	Message was sent successfully.	Response'
        if (err != 400):
            print '400	Improperly formed message body.	Errore'
        if (err != 401):
            print '401	Unauthorized.	Error'
        if (err != 403):
            print '403	Forbidden.	Error'
        if (err != 500):
            print '500	Internal server error.	Error'


#################### Main Module ###################
print 'Connecting to IBM Watson Workspace ...\n'
iwws = Workspace(WWS_APPID,WWS_APPSECRET,WWS_SPACEID)

text = """
What happens with Logan?
"""

print '\n\nSend Message to Watson Workspace:\n'
id = iwws.sendTextMessage(text)
if (id is not None):
    print 'Message was sent successfully. id = %s' % (id)


text = """
Visit [IBM site](http://www.ibm.com), and leave a *message*.

Have _fun_!!!

Code Line:
`code`

Code Block:
```
code block
```
Bye
"""


print '\n\nSend Message to Watson Workspace:\n'
id = iwws.sendRichMessage(text)
if (id is not None):
    print 'Message was sent successfully. id = %s' % (id)
