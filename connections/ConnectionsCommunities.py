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
CONNECTIONS_PASSWORD = '<REPLACE_HERE>


# Disable Warnings from Untrusted TLs keys
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ConnectionsCommunities:

    def __init__(self,hostname=None,loginname=None,password=None):
        self.hostname = hostname
        self.loginname = loginname
        self.password = password

    def doGet(self,url,headers,auth):
        r = requests.get(url=url,headers=headers,auth=auth, verify=False)
        if (r.status_code != 200):
            print 'requests.get -> %s = %s\n' % (r.url, r)
            return None;
        return r.content

    def parseOpensearch(self,content):

        opensearch = {
            'totalResults': 0,
            'startIndex': 0,
            'itemsPerPage': 0,
            'pages': 0
        }

        root = ET.fromstring(content)

        temp = root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults")
        if (temp is None):
            return opensearch
        totalResults = int(temp.text)

        temp = root.find("{http://a9.com/-/spec/opensearch/1.1/}startIndex")
        if (temp is None):
            return opensearch
        startIndex = int(temp.text)

        temp = root.find("{http://a9.com/-/spec/opensearch/1.1/}itemsPerPage")
        if (temp is None):
            return opensearch
        itemsPerPage = int(temp.text)

        pages = totalResults / itemsPerPage
        if ((totalResults % itemsPerPage) != 0):
            pages = pages + 1

        opensearch = {
            'totalResults': totalResults,
            'startIndex': startIndex,
            'itemsPerPage': itemsPerPage,
            'pages': pages
        }
        return opensearch

    def parseCommunities(self,content,communities):

        root = ET.fromstring(content)
        entries = root.findall("{http://www.w3.org/2005/Atom}entry")
        for entry in entries:
            communityUuid = entry.find('{http://www.ibm.com/xmlns/prod/sn}communityUuid').text
            title = entry.find('{http://www.w3.org/2005/Atom}title').text

            contributor = entry.find('{http://www.w3.org/2005/Atom}contributor')
            t_email= contributor.find('{http://www.w3.org/2005/Atom}email')
            email = ''
            if (t_email is not None):
                email = t_email.text

            community = {
            'uuid': communityUuid,
            'title': title.encode("utf-8"),
            'email': email
            }
            communities.append(community)

    def listAll(self):
        communities = []

        url = self.hostname + '/communities/service/atom/communities/all?page=1'
        headers = { 'Content-Type': 'atom/xml'}
        auth=HTTPBasicAuth(self.loginname, self.password)

        feedCommunities = self.doGet(url=url,headers=headers,auth=auth)
        if (feedCommunities is None):
            return None
        #print feedCommunities

        opensearch = self.parseOpensearch(feedCommunities)

        if (opensearch['pages'] == 0):
            return None

        print url
        self.parseCommunities(feedCommunities,communities)
    
        max = opensearch['pages'] + 1
        for page in range(2,max):
            url = self.hostname + '/communities/service/atom/communities/all?page=' + str(page);
            if (page % 50 == 0):
                print url
            feedCommunities = self.doGet(url=url,headers=headers,auth=auth)
            if (feedCommunities is None):
                return None
            self.parseCommunities(feedCommunities,communities)
        print url
        return communities

    def getCommunityOwners(self,communityUuid):
        url = self.hostname + '/communities/service/atom/community/members?communityUuid=' + communityUuid
        headers = { 'Content-Type': 'atom/xml'}
        auth=HTTPBasicAuth(self.loginname, self.password)

        feedMembers = self.doGet(url=url,headers=headers,auth=auth)
        if (feedMembers is None):
            return None

        members = self.parseMembers(feedMembers)
        if (members is None):
            return None

        owners = []
        for m in members:
            if m['role'] == 'owner':
                owners.append(m)
        return owners

    def parseMembers(self,feed):
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

cc =  ConnectionsCommunities(CONNECTIONS_HOST,CONNECTIONS_USERNAME,CONNECTIONS_PASSWORD)

communities = cc.listAll()

if (communities is None):
    print 'Cannot get Connections Communities.'
    sys.exit(1)

for community in communities:
    owners = cc.getCommunityOwners(community['uuid'])
    if (owners is not None):
        community['owners'] = owners


f = open('communities.txt', 'w')
f.write('List Communities and Owners\n')
i = 1
for c in communities:
    f.write( '%s) %s\n' % (i,c['title']) )
    i = i + 1
    f.write( ' |--> uuid: %s\n' % c['uuid'] )
    f.write( ' |--> email: %s\n' % c['email'] )
    for o in c['owners']:
        f.write( ' |----> owner: %s\n' % (o['email']))
    f.write( '\n')
f.close()
