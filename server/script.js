
const googleTranslateTKK = "448487.932609646";

function shiftLeftOrRightThenSumOrXor(num, optString) {
    for (let i = 0; i < optString.length - 2; i += 3) {
        let acc = optString.charAt(i + 2);
        if ('a' <= acc) {
            acc = acc.charCodeAt(0) - 87;
        } else {
            acc = Number(acc);
        }
        if (optString.charAt(i + 1) == '+') {
            acc = num >>> acc;
        } else {
            acc = num << acc;
        }
        if (optString.charAt(i) == '+') {
            num += acc & 4294967295;
        } else {
            num ^= acc;
        }
    }
    return num;
}

function transformQuery(query) {
    const bytesArray = [];
    let idx = [];
    for (let i = 0; i < query.length; i++) {
        let charCode = query.charCodeAt(i);

        if (128 > charCode) {
            bytesArray[idx++] = charCode;
        } else {
            if (2048 > charCode) {
                bytesArray[idx++] = charCode >> 6 | 192;
            } else {
                if (55296 == (charCode & 64512) && i + 1 < query.length && 56320 == (query.charCodeAt(i + 1) & 64512)) {
                    charCode = 65536 + ((charCode & 1023) << 10) + (query.charCodeAt(++i) & 1023);
                    bytesArray[idx++] = charCode >> 18 | 240;
                    bytesArray[idx++] = charCode >> 12 & 63 | 128;
                } else {
                    bytesArray[idx++] = charCode >> 12 | 224;
                }
                bytesArray[idx++] = charCode >> 6 & 63 | 128;
            }
            bytesArray[idx++] = charCode & 63 | 128;
        }

    }
    return bytesArray;
}

function calcHash(query, windowTkk) {
    const tkkSplited = windowTkk.split('.');
    const tkkIndex = Number(tkkSplited[0]) || 0;
    const tkkKey = Number(tkkSplited[1]) || 0;

    const bytesArray = transformQuery(query);

    let encondingRound = tkkIndex;
    for (const item of bytesArray) {
        encondingRound += item;
        encondingRound = shiftLeftOrRightThenSumOrXor(encondingRound, '+-a^+6');
    }
    encondingRound = shiftLeftOrRightThenSumOrXor(encondingRound, '+-3^+b+-f');

    encondingRound ^= tkkKey;
    if (encondingRound <= 0) {
        encondingRound = (encondingRound & 2147483647) + 2147483648;
    }

    const normalizedResult = encondingRound % 1000000;
    return normalizedResult.toString() + '.' + (normalizedResult ^ tkkIndex);
}


// var http = require('http');
// var url = require('url');

// http.createServer(function (req, res) {
//     res.writeHead(200, {'Content-Type': 'text/html'});
//     /*Use the url module to turn the querystring into an object:*/
//     var q = url.parse(req.url, true).query;
//     /*Return the year and month from the query object:*/
//     var token = calcHash(q.text,googleTranslateTKK);
//     res.end(token);
//     console.log('------')
//     console.log(token)
// }).listen(14756);
//-----------------------------------------------
// text = "change the world"
// function escapeHTML(unsafe) {
//     return unsafe
//         .replace(/\&/g, "&amp;")
//         .replace(/\</g, "&lt;")
//         .replace(/\>/g, "&gt;")
//         .replace(/\"/g, "&quot;")
//         .replace(/\'/g, "&#39;");
// }

// function unescapeHTML(unsafe) {
//     return unsafe
//         .replace(/\&amp;/g, "&")
//         .replace(/\&lt;/g, "<")
//         .replace(/\&gt;/g, ">")
//         .replace(/\&quot;/g, "\"")
//         .replace(/\&\#39;/g, "'");
// }
// console.log(escapeHTML(text))
// console.log(calcHash(escapeHTML(text),googleTranslateTKK))


var express = require('express');
var bodyParser = require('body-parser')

var app = express();

app.use(bodyParser.urlencoded({
    extended: true
}));

var i = 0
app.post('/', function(request, response){
 	let myJson = request.body;
    // console.log(myJson)
    console.log("I RECEIVED I REQUEST N" + i)
    i++
    var token = calcHash(request.body.text,googleTranslateTKK);
    
	response.send(token);
    	 
});

app.listen(14756);