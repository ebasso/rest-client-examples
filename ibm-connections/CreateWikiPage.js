/*
 * Antes de executar:
 *
 * > npm install request
 * > npm install xml2js
 *
 *
 */
'use strict';
// Ignore self signed certificates
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const request = require('request');
const xml2js = require('xml2js');
const parser = new xml2js.Parser();

const CONNECTIONS_HOST = 'https://connections.<REPLACE_HERE>.com';
const CONNECTIONS_USERNAME = '<REPLACE_HERE>';
const CONNECTIONS_PASSWORD = '<REPLACE_HERE>';

// For Wikis inside a community -> https://{hostname}/wikis/home?lang=en-us#!/wiki/W34c618febb3c_4a55_81b7_0d5a81dc1954
// For Wikis outside a community -> https://{hostname}/wikis/home?lang=en-us#!/wiki/User Guide
var wiki_id_or_label = 'W34c618febb3c_4a55_81b7_0d5a81dc1954';

function createWikiPage(wiki_id_or_label) {

    var body = '';
    body += '<entry xmlns="http://www.w3.org/2005/Atom">';
    body += '<title type="text">My First Wiki</title>';
    body += '<content type="text/html">';
    body += '<![CDATA[<?xml version="1.0" encoding="UTF-8"?><p>';
    body += '<strong>Hello World!</strong>';
    body += '</p>]]>';
    body += '</content>';
    body += '<category term="wikipagetag1" />';
    body += '<category term="wikipagetag2" />';
    body += 'category scheme="tag:ibm.com,2006:td/type" term="page" label="page" />';
    body += '</entry>';

    var options = {
        url: CONNECTIONS_HOST + '/wikis/basic/api/wiki/' + wiki_id_or_label  + '/feed',
        auth: {
            username: CONNECTIONS_USERNAME,
            password: CONNECTIONS_PASSWORD
        },
        headers: {
            'Content-Type': 'application/atom+xml;charset=UTF-8'
        },
        body: body
    };

    request.post(options, function(error, response, body) {
        if (error) {
            console.error('error --> ');
            console.error(error);
        }
       if (response.statusCode >= 200 && response.statusCode < 300) {
            console.log('Success')
            console.error('response.statusCode --> ', response.statusCode);
            console.error('body --> ');
            console.error(body);
            console.error('\n');
        } else {
            console.log('Failed')
            console.error('response.statusCode --> ', response.statusCode);
            console.error('body --> ');
        }


     });
}


//******************************     MAIN          **********************************//
console.log('Connecting to IBM Connections...\n');
console.log('Creating Wiki Page...\n');
createWikiPage(wiki_id_or_label);
