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
var communityUuid = 'c5e4747d-3177-4c30-884a-7a150e7bebef';


function getCommunityOwners(communityUuid) {
    var options = {
        url: CONNECTIONS_HOST + '/communities/service/atom/community/members?communityUuid=' + communityUuid,
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

        var members = parseMembers(body);
        if (!members) {
            return;
        }

        var owners = [];
        for (let i = 0, len = members.length; i < len; i++) {
            if (members[i].role == 'owner') {
                owners.push(members[i]);
            }
        }
        printOwners(communityUuid, owners);
    });
}

function parseMembers(body) {
    var extractedData = [];
    parser.parseString(body, function(err, result) {
        if (err) {
            console.log(err);
            console.error('parseMembers: Cannot parse ProfileInfo ');
            return;
        }
        if (!result.feed.entry) {
            console.error('parseMembers: Missing <ENTRY> element');
            return;
        }

        for (let index = 0, len = result.feed.entry.length; index < len; ++index) {
            var email = result.feed.entry[index].contributor[0].email[0];
            var role = result.feed.entry[index]['snx:role'][0]._;
            //console.log(role);

            var member = {
                email: email,
                role: role
            };
            extractedData.push(member);
        }
    });

    return extractedData;
}

function printOwners(communityUuid, owners) {

    console.log('List Community Owners');
    console.log(communityUuid);
    for (let i = 0, len = owners.length; i < len; i++) {
        console.log(' |--> email: ' + owners[i].email);
    }
}

//******************************     MAIN          **********************************//
console.log('Connecting to IBM Connections...');
getCommunityOwners(communityUuid);
