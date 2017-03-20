/*
 * Before Execute
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

function getConnectionsCommunities() {
    var options = {
        url: CONNECTIONS_HOST + '/communities/service/atom/communities/all',
        auth: {
            username: CONNECTIONS_USERNAME,
            password: CONNECTIONS_PASSWORD
        },
        headers: {
            'Content-Type': 'application/atom+xml;charset=UTF-8'
        }
    };

    request.get(options, function(error, response, body) {
        if (error || response.statusCode != 200) {
            console.error('Failed to contact Connections Server');
            return;
        }
        var communities = parseCommunities(body);
        printCommunities(communities);
    });
}

function parseCommunities(body) {
    var extractedData = [];
    parser.parseString(body, function(err, result) {
        if (err) {
            console.log(err);
            console.error('parseCommunities: Cannot parse ProfileInfo ');
            return;
        }
        if (!result.feed.entry) {
            console.error('parseCommunities: Missing <ENTRY> element');
            return;
        }
        for (let index = 0, len = result.feed.entry.length; index < len; ++index) {

            var uuid = result.feed.entry[index]['snx:communityUuid'];
            var title = result.feed.entry[index].title[0]._;
            var email = result.feed.entry[index].contributor[0].email[0];
            //console.log(uuid + ' -- ' + title + ' -- ' + email);
            var community = {
                uuid: uuid,
                title: title,
                email: email
            };
            extractedData.push(community);
        }
    });
    return extractedData;
}


function printCommunities(communities) {
    console.log('List Communities');

    for (let i = 0, len = communities.length; i < len; i++) {
        console.log(communities[i].title);
        console.log(' |--> uuid: ' + communities[i].uuid);
        console.log(' |--> email: ' + communities[i].email);
    }
}

//******************************     MAIN          **********************************//
console.log('Connecting to IBM Connections...');
getConnectionsCommunities();
