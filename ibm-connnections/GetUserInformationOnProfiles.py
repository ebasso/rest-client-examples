# -*- coding: utf-8 -*-
#
# Antes de executar:
#
# > pip install requests
#
#
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET

CONNECTIONS_HOST = 'https://connections.<REPLACE_HERE>.com'
CONNECTIONS_USERNAME = '<REPLACE_HERE>'
CONNECTIONS_PASSWORD = '<REPLACE_HERE>'
QUERY = 'email=smith@<REPLACE_HERE>.com'
# Other options for QUERY
# 1) email=<email_address>
# 2) uuid=<uuid of user>
# 3) uid=<uid of user>

DEBUG=0

# Disable Warnings from Untrusted TLs keys
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Disable Warnings from Untrusted TLs keys
def doGet(url,headers,auth):
    res = requests.get(url=url,headers=headers,auth=auth, verify=False)
    if (res.status_code != 200):
        print 'requests.get -> %s = %s\n' % (res.url, res)
        return None;
    #print res.content
    return res.content

def parseProfileIfno(content):

    root = ET.fromstring(content)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    contributor = entry.find('{http://www.w3.org/2005/Atom}contributor')
    name = contributor.find('{http://www.w3.org/2005/Atom}name').text
    # for namespace snx:userid change to http://www.ibm.com/xmlns/prod/sn
    userid = contributor.find('{http://www.ibm.com/xmlns/prod/sn}userid').text
    email = contributor.find('{http://www.w3.org/2005/Atom}email').text
    userState = contributor.find('{http://www.ibm.com/xmlns/prod/sn}userState').text

    profile = {
    'name': name,
    'userid': userid,
    'email': email,
    'userState': userState
    }
    #print profile
    return profile

def getProfileInfo(query):
    url = CONNECTIONS_HOST + '/profiles/atom/profile.do?' + query
    print url + '\n'
    headers = { 'Content-Type': 'application/atom+xml;charset=UTF-8'}
    auth=None

    feed = doGet(url=url,headers=headers,auth=auth)
    if (feed is None):
        return None
    return parseProfileIfno(feed)

#################### Main Module ###################
print 'Connecting to IBM Connections...\n'
if (DEBUG == 1):
    print sys.stdout.encoding + '\n\n'

profile = getProfileInfo(QUERY)

if (profile is None):
    print 'Cannot get Profile Information.'
    sys.exit(1)

print 'Profile Information:\n'
print profile['name']
print ' |--> userid: ' + profile['userid']
print ' |--> email: ' + profile['email']
print ' |--> userState: ' + profile['userState']
