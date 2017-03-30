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
        url = self.hostname + '/stmeetings/restapi'
        headers = { 'Accept': 'text/json', 'X-ST-CSRF-Token': self.csrfToken }
        res = self.session.post(url=url,headers=headers,data=data)

        if (res.status_code != 200):
            print 'createRoom -> %s = %s\n' % (res.url, res)
            print res.content
            return None;
        #print '-------------------------------------- res.content'
        #print res.content
        if (res.headers['Content-Type'] != 'text/json'):
            print 'createRoom: No Json returned'
            return None

        return res.json()

    def getRoom(self,uuid=None):

        if (uuid is None):
            return None

        if (self.doAuth() is None):
            return None

        #data = { 'id': uuid }
        params = { 'dojo.preventCache': str(time.time())  }
        url = self.hostname + '/stmeetings/restapi?id=' + uuid
        headers = { 'Accept': 'text/json', 'X-ST-CSRF-Token': self.csrfToken }
        res = self.session.get(url=url,headers=headers)#,data=data)

        #print res.content
        if (res.status_code != 200):
            print 'getRoom -> %s = %s\n' % (res.url, res)
            print res.content
            return None;
        #print '-------------------------------------- res.content'
        #print res.content
        if (res.headers['Content-Type'] != 'text/json'):
            print 'getRoom: No Json returned'
            return None

        return res.json()

    def updateRoom(self,data):

        if (self.doAuth() is None):
            return None

        params = { 'dojo.preventCache': str(time.time())  }
        url = self.hostname + '/stmeetings/restapi'#?'+ urllib.urlencode(params);
        headers = { 'Accept': 'text/json', 'X-ST-CSRF-Token': self.csrfToken }
        res = self.session.post(url=url,headers=headers,data=data)

        if (res.status_code != 200):
            print 'updateRoom -> %s = %s\n' % (res.url, res)
            print res.content
            return None;
        #print '-------------------------------------- res.content'
        print res.content
        if (res.headers['Content-Type'] != 'text/json'):
            print 'updateRoom: No Json returned'
            return None

        return res.json()

    def deleteRoom(self,uuid=None):

        if (uuid is None):
            return None

        if (self.doAuth() is None):
            return None

        params = { 'dojo.preventCache': str(time.time())  }
        url = self.hostname + '/stmeetings/restapi?id=' + uuid
        headers = { 'Accept': 'text/json', 'X-ST-CSRF-Token': self.csrfToken }
        res = self.session.delete(url=url,headers=headers)

        if (res.status_code != 200):
            print 'deleteRoom -> %s = %s\n' % (res.url, res)
            print res.content

        return res.status_code

    def listMyRooms():

        if (self.doAuth() is None):
            return None

        url = self.hostname + '/stmeetings/restapi?myRooms=true&sortKey=meetingName&sortOrder=ascending&count=10&start=1&dojo.preventCache=' + str(time.time())
        headers = { 'Content-Type': 'text/json'}
        res =self.session.get(url,headers=headers)

        if (res.status_code != 200):
            print 'listMyRooms -> %s = %s\n' % (r.url, r)
            return None
        if (res.headers['Content-Type'] != 'text/json'):
            print 'listMyRooms: No Json returned'
            return None

        return res.json()

    def listRoomsByOrigin(self,originId=None,originType=None):

        if ((originId is None) or (originType is None)):
            return None

        if (self.doAuth() is None):
            return None

        url = self.hostname + '/stmeetings/restapi?originId=' + originId + '&originType=' + originType + '&dojo.preventCache=' + str(time.time())
        headers = { 'Content-Type': 'text/json'}
        res =self.session.get(url,headers=headers)

        if (res.status_code != 200):
            print 'listRoomsByOrigin -> %s = %s\n' % (r.url, r)
            return None
        if (res.headers['Content-Type'] != 'text/json'):
            print 'listRoomsByOrigin: No Json returned'
            return None

        return res.json()


def printRoom(room):

    if (room is None):
        print 'Room: Not created or not exit'
        return None

    print '%s' % room['name']
    print ' |--> id: %s' % room['id']
    print ' |--> joinPath: %s' % room['joinPath']
    print ' |--> permaName: %s' % room['permaName']
    print ' |--> owner: %s' % room['owner']
    for manager in room['managersList']:
        print ' |----> manager: %s' % manager
    print '\n'

#################### Main Module ###################
print 'Connecting to IBM Sametime Meetings ...\n'

stmeetings = SametimeMeetings(MEETINGS_HOST,MEETINGS_USERNAME,MEETINGS_PASSWORD)

#--------------------  Create Room --------------------
DRAFT_ROOM = {
'name': 'PythonMeeting ==>' + str(time.time()), # Required
'description': 'Meeting create by SametimeMeetingRoom.py',
'originType': 'Python',
'originId': 'Python',
'owner': 'wsadmin@ibm.com'
}
print 'Create Meetings\n'
room = stmeetings.createRoom(DRAFT_ROOM)
printRoom(room)


#print '-------------------------------------\n\n'


#--------------------  Get Room --------------------
#roomId = 'a3eeb03b-77f9-4baa-a1bf-de491fe20e97'
#print 'Get Room \n'
#room = stmeetings.getRoom(roomId)
#print room['results'][0]['id']
#print '-------------------------------------\n\n'


#--------------------  Update Room --------------------
#DRAFT_ROOM = {
#'id': roomId,
#'description': 'Meeting updated by SametimeMeetingRoom.py'
#}
#print 'Update Room \n'
#room = stmeetings.updateRoom(DRAFT_ROOM)
#print room['id']
#print '-------------------------------------\n\n'


#--------------------  Delete Room --------------------
#roomId = 'a3eeb03b-77f9-4baa-a1bf-de491fe20e97'
#print stmeetings.deleteRoom(roomId)


#--------------------  List Room --------------------
print 'List Room \n'
rooms = stmeetings.listRoomsByOrigin('Python','Python')
for room in rooms['results']:
    printRoom(room)
print '-------------------------------------\n\n'
