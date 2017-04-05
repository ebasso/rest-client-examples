# -*- coding: utf-8 -*-
#
# Necessary libraries:
#
# > pip install requests
#
# url = MEETINGS_HOST + '/stmeetings/restapi?' + parameters
# Where parameters:
#   myRooms=true
#   &sortKey=meetingName
#   &sortOrder=ascending
#   &count=10
#   &start=1
#   &dojo.preventCache=NNNNNNNNN
#
import sys, time, json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth

MEETINGS_HOST = 'https://stproxy.<REPLACE_HERE>.com'
MEETINGS_USERNAME = '<REPLACE_HERE>'
MEETINGS_PASSWORD = '<REPLACE_HERE>'
DEBUG=0

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def doAuth():
    url = MEETINGS_HOST + '/stmeetings/j_security_check'

    session = requests.session()
    payload = {'j_username': MEETINGS_USERNAME, 'j_password': MEETINGS_PASSWORD}
    res = session.post(url, data=payload, verify=False)
    if (res.status_code != 200):
        print 'doAuth: requests.get -> %s = %s\n' % (res.url, res)
        return None

    if (u"var userName = \"" not in res.text):
        print 'doAuth: Login Error no userName'
        return None
    return session

def getMeetingsFromUser():
    session = doAuth()
    if (session is None):
        return None

    url = MEETINGS_HOST + '/stmeetings/restapi?myRooms=true&sortKey=meetingName&sortOrder=ascending&count=10&start=1&dojo.preventCache=%s' % int(time.time())
    headers = { 'Content-Type': 'text/json'}
    res = session.get(url,headers=headers)

    if (res.status_code != 200):
        print 'getMeetingsFromUser: requests.get -> %s = %s\n' % (r.url, r)
        return None
    if (res.headers['Content-Type'] != 'text/json'):
        print 'getMeetingsFromUser: No Json returned'
        return None

    return res.json()

# Todo:
def searchMeetings():
    #If you have admin access, you can then drill down further such as
    #url = MEETINGS_HOST + '/stmeetings/restapi?search=Enio%20Basso&searchType=listed&sortKey=meetingName&sortOrder=ascending&count=10&start=1​
    return None

#################### Main Module ###################
print 'Connecting to IBM Sametime Meetings ...\n'
if (DEBUG == 1):
    print sys.stdout.encoding + '\n\n'

#originId = ''
#originType = ''
#feedCommunities = doGetMeetings(originId,originType)
meetingsResponse = getMeetingsFromUser()

if (meetingsResponse is None):
    print 'Cannot get Sametime Meetings.'
    sys.exit(1)

if (meetingsResponse['count'] == 0):
    print 'No meeting rooms!'
    sys.exit(0)

meetingRooms = meetingsResponse['results']

print 'List Meetings and Managers\n'
for mr in meetingRooms:
    print mr['name']
    print ' |--> joinPath: ' + mr['joinPath']
    for o in mr['managersList']:
        print ' |----> manager: %s' % (o)
    print
