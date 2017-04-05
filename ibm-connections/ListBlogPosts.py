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

CONNECTIONS_HOST = 'https://connections.<company>.com'
CONNECTIONS_USERNAME = '<REPLACE_HERE>'
CONNECTIONS_PASSWORD = '<REPLACE_HERE>'

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

def parsePostDetails(content):

    entry = ET.fromstring(content)

    #entry = root.find('{http://www.w3.org/2005/Atom}entry')
    #print '------------------------------------------------------------------------------------------------------------------------------------------------------'
    #for child in entry:
    #    print child.tag, child.attrib
    #print '------------------------------------------------------------------------------------------------------------------------------------------------------'
    title = entry.find('{http://www.w3.org/2005/Atom}title').text
    author = entry.find('{http://www.w3.org/2005/Atom}author')
    name = author.find('{http://www.w3.org/2005/Atom}name').text
    email = author.find('{http://www.w3.org/2005/Atom}email').text

    blogPost = {
    'title': title.encode("cp850"),
    'name': name,
    'email': email
    }
    #print profile
    return blogPost

def getPostDetails(handle=None,entryId=None):
    if (handle == None or entryId == None):
        return None
    url = '%s/blogs/%s/api/entries/%s' % (CONNECTIONS_HOST,handle,entryId)
    headers = { 'Content-Type': 'application/atom+xml;charset=UTF-8'}
    auth=HTTPBasicAuth(CONNECTIONS_USERNAME, CONNECTIONS_PASSWORD)

    feed = doGet(url=url,headers=headers,auth=auth)
    if (feed is None):
        return None
    blogPost =  parsePostDetails(feed)

    if (blogPost is None):
        print 'Cannot get Blog Post Information.'
        return None

    print 'Post Details:\n'
    print blogPost['title']
    print ' |--> name: ' + blogPost['name']
    print ' |--> email: ' + blogPost['email']

def parseBlogPosts(content):
    posts = []

    root = ET.fromstring(content)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    for entry in entries:
        entryId = entry.find('{http://www.w3.org/2005/Atom}id').text
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        author = entry.find('{http://www.w3.org/2005/Atom}author')
        name = author.find('{http://www.w3.org/2005/Atom}name').text
        email = author.find('{http://www.w3.org/2005/Atom}email').text

        #urn:lsid:ibm.com:blogs:entry-048667f2-400b-4b70-8c04-cc163403cba6
        entryId = entryId[-36:]
        post = {
        'entryId': entryId,
        'title': title.encode('utf-8'),
        'name': name,
        'email': email
        }
        posts.append(post)
    return posts

def getBlogPosts(handle=None):
    if (handle == None):
        return None
    url = '%s/blogs/%s/api/entries' % (CONNECTIONS_HOST,handle)
    headers = { 'Content-Type': 'application/atom+xml;charset=UTF-8'}
    auth=HTTPBasicAuth(CONNECTIONS_USERNAME, CONNECTIONS_PASSWORD)

    feed = doGet(url=url,headers=headers,auth=auth)
    if (feed is None):
        return None
    posts =  parseBlogPosts(feed)

    if (posts is None):
        return None
    return posts

#################### Main Module ###################
print 'Connecting to IBM Connections...\n'

handle = 'ce8716a1-3575-44fd-8b2e-4f5360fe03e1'
#entryId = '66ce5af8-d7e2-451c-9435-3f236accfc12'
#getPostDetails(handle,entryId)

posts = getBlogPosts(handle)
if (posts is None):
    print 'Cannot get Blog Posts Information.'
    sys.exit(1)

print 'Blog Posts:\n'
for post in posts:
    print post['entryId']
    print ' |--> name: ' + post['title']
    print ' |--> name: ' + post['name']
    print ' |--> email: ' + post['email']
    print
