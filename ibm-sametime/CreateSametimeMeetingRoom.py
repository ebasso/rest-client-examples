#!/usr/local/bin/python2.7
# encoding: utf-8

# Necessary libraries:
#
# > pip install requests
#
#
import sys, time, json, re
import requests,urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

MEETINGS_HOST = 'https://meeting.COMPANY.COM'
MEETINGS_USERNAME = '<REPLACE_HERE>'
MEETINGS_PASSWORD = '<REPLACE_HERE>'

DRAFT_ROOM = {
'name': 'PythonMeeting ==>' + str(time.time()),
'description': 'Meeting create by CreateSametimeMeetingRoom.py',
'originType': 'Python',
'originId': 'Python',
'owner': 'wsadmin@ibm.com'
}

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class SametimeMeetings:

    def __init__(self,hostname=None,loginname=None,password=None):
        self.hostname = hostname
        self.loginname = loginname
        self.password = password
        self.username = None
        self.csrfToken = None
        self.session = None

    def doAuth(self):

        # If already has token return session
        if (self.csrfToken is not None):
            return self.session

        url = self.hostname + '/stmeetings/j_security_check'

        session = requests.session()
        payload = {'j_username': self.loginname, 'j_password': self.password}
        res = session.post(url, data=payload, verify=False)

        if (res.status_code != 200):
            print 'doAuth: requests.get -> %s = %s\n' % (res.url, res)
            return None

        if (res.headers['Content-Type'] != 'text/html;charset=UTF-8'):
            print 'doAuth: Not expected -> "Content-Type": "' + res.headers['Content-Type'] + '"'
            return None

        if (u"var userName = \"" not in res.text):
            print 'doAuth: Login Error no userName'
            return None

        html = str(res.text.encode('utf-8'))
        #var userName = "wsadmin@COMPANY.com";
        start = html.find('var userName = \"') + 16
        end = html.find('";', start)
        self.username = html[start:end]

        #var csrfToken = "53cb34906d36e6d5d0682c526b8a5bd0";
        start = html.find('var csrfToken = \"') + 17
        end = html.find('";', start)
        self.csrfToken = html[start:end]
        self.session = session
        return session


    def createRoom(self,data):

        if (self.doAuth() is None):
            return None

        params = { 'dojo.preventCache': str(time.time())  }
        url = self.hostname + '/stmeetings/restapi'#?'+ urllib.urlencode(params);
        headers = { 'Accept': 'text/json', 'X-ST-CSRF-Token': self.csrfToken }
        res = self.session.post(url=url,headers=headers,data=data)

        if (res.status_code != 200):
            print 'createRoom: requests.post -> %s = %s\n' % (res.url, res)
            print res.content
            return None;
        #print '-------------------------------------- res.content'
        #print res.content
        if (res.headers['Content-Type'] != 'text/json'):
            print 'createRoom: No Json returned'
            return None

        return res.json()

#################### Main Module ###################
print 'Connecting to IBM Sametime Meetings ...\n'

stmeetings = SametimeMeetings(MEETINGS_HOST,MEETINGS_USERNAME,MEETINGS_PASSWORD)
room = stmeetings.createRoom(DRAFT_ROOM)

if (room is None):
    print 'Room: Not created'

print room['name']
print ' |--> id: ' + room['id']
print ' |--> joinPath: ' + room['joinPath']
print ' |--> permaName: ' + room['permaName']
print ' |--> owner: ' + room['owner']
print ' |--> ownerName: ' + room['ownerName']
for manager in room['managersList']:
    print ' |----> manager: ' + manager
