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

CONNECTIONS_HOST = '<REPLACE_HERE>'
CONNECTIONS_USERNAME = '<REPLACE_HERE>'
CONNECTIONS_PASSWORD = '<REPLACE_HERE>
DEBUG=0

# Disable Warnings from Untrusted TLs keys
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Disable Warnings from Untrusted TLs keys
def doGet(url,headers,auth):
    r = requests.get(url=url,headers=headers,auth=auth, verify=False)
    if (r.status_code != 200):
        print 'requests.get -> %s = %s\n' % (r.url, r)
        return None;
    return r.content

def parseCommunities(content):
    communities = []
    
    root = ET.fromstring(content)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    for entry in entries:
        snx_comm = entry.find('{http://www.ibm.com/xmlns/prod/sn}communityUuid')
        communityUuid = snx_comm.text

        snx_title = entry.find('{http://www.w3.org/2005/Atom}title')
        title = snx_title.text

        contributor = entry.find('{http://www.w3.org/2005/Atom}contributor')
        t_email= contributor.find('{http://www.w3.org/2005/Atom}email')
        email = ''
        if (t_email is not None):
            email = t_email.text

        community = {
        'uuid': communityUuid,
        'title': title.encode("cp850"),
        'email': email
        }
        communities.append(community)

    return communities

def getConnectionsCommunities():
    url = CONNECTIONS_HOST + '/communities/service/atom/communities/all'
    headers = { 'Content-Type': 'atom/xml'}
    auth=HTTPBasicAuth(CONNECTIONS_USERNAME, CONNECTIONS_PASSWORD)

    feedCommunities = doGet(url=url,headers=headers,auth=auth)
    if (feedCommunities is None):
        return None
    return parseCommunities(feedCommunities)


def getCommunityOwners(communityUuid):
    url = CONNECTIONS_HOST + '/communities/service/atom/community/members?communityUuid=' + communityUuid
    headers = { 'Content-Type': 'atom/xml'}
    auth=HTTPBasicAuth(CONNECTIONS_USERNAME, CONNECTIONS_PASSWORD)

    feedMembers = doGet(url=url,headers=headers,auth=auth)
    if (feedMembers is None):
        return None

    members = parseMembers(feedMembers)
    if (members is None):
        return None

    owners = []
    for m in members:
        if m['role'] == 'owner':
            owners.append(m)

    return owners

def parseMembers(feed):
    members = []
    root = ET.fromstring(feed)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    for entry in entries:
        contributor = entry.find('{http://www.w3.org/2005/Atom}contributor')
        t_email= contributor.find('{http://www.w3.org/2005/Atom}email')

        if (t_email is not None):
            email = t_email.text
            #print email

            role = entry.find('{http://www.ibm.com/xmlns/prod/sn}role').text
            #print role
            member = {
            'email': email,
            'role': role
            }
            members.append(member)

    return members

#################### Main Module ###################
print 'Connecting to IBM Connections...\n'
if (DEBUG == 1):
    print sys.stdout.encoding + '\n\n'

communities = getConnectionsCommunities()

if (communities is None):
    print 'Cannot get Connections Communities.'
    sys.exit(1)

for c in communities:
    owners = getCommunityOwners(c['uuid'])
    if (owners is not None):
        c['owners'] = owners

print 'List Communities and Owners\n'
for c in communities:
    print c['title']
    print ' |--> uuid: ' + c['uuid']
    print ' |--> email: ' + c['email']
    for o in c['owners']:
        print ' |----> owner: %s' % (o['email'])
    print
