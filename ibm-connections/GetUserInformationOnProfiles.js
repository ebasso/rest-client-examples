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
const QUERY = 'email=smith@<REPLACE_HERE>.com';
/*
 * Other options for QUERY
 *  1) email=<email_address>
 * 2) uuid=<uuid of user>
 * 3) uid=<uid of user>
 */

function getProfileInfo() {
    var options = {
        url: CONNECTIONS_HOST + '/profiles/atom/profile.do?' + QUERY,
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
            console.error('Failed to contact Connections Server\n');
            console.error(error);
            return;
        }

        var profile = parseProfileInfo(body);
        if (!profile) {
            return;
        }
        printProfile(profile);
    });
}

function parseProfileInfo(body) {
    var profile = {};
    parser.parseString(body, function(err, result) {
        if (err) {
            console.log(err);
            console.error('parseProfileInfo: Cannot parse ProfileInfo ');
            return;
        }
        if (!result.feed.entry) {
            console.error('parseProfileInfo: Missing <ENTRY> element');
            return;
        }

        profile['name'] = result.feed.entry[0].contributor[0]['name'][0];
        profile['email'] = result.feed.entry[0].contributor[0]['email'][0];
        profile['userid'] = result.feed.entry[0].contributor[0]['snx:userid'][0];
        profile['userState'] = result.feed.entry[0].contributor[0]['snx:userState'][0];
    });
    return profile;
}

function printProfile(profile) {
    console.log('Profile Information:');
    console.log(profile['name']);
    console.log(' |--> userid: ' + profile['userid']);
    console.log(' |--> email: ' + profile['email']);
    console.log(' |--> userState: ' + profile['userState']);
}

//******************************     MAIN          **********************************//
console.log('Connecting to IBM Connections...\n');
getProfileInfo();
