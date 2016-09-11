var express = require('express');
var app = express();
var fs = require("fs");
var https = require('https');
var webshot = require('./lib/node-webshot-master/lib/webshot');

// var $ = require('jquery');
app.use(express.static('public'));

// This responds with "Hello World" on the homepage
app.get('/', function (req, res) {
   console.log("Got a GET request for the homepage");
   res.send('Hello GET');
})

// This responds a GET request for the /list_user page.
app.get('/get_map', function (req, res) {
    console.log("Got a GET request for /get_map");
    var url = require('url');
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;
    var params = query.src+"\n"+query.dest;

    fs.writeFile( __dirname + "/public/" + "location.js", params, function(err) {
      if(err) {
          return console.log(err);
      }
    }); 

    fs.readFile( __dirname + "/public/" + "index.html", 'utf8', function (err, data) {
      res.send( data );
    });
});

app.get('/get_nearby', function (req, res) {
   console.log("Got a GET request for /get_nearby");
   var nearbyOptionsMap = {
     "1": {name:"Restaurants", sic_code:581208},
     "2": {name:"Cafes", sic_code:581214},
     "3": {name:"Bars", sic_code:581301},
     "4": {name:"Ice Cream Parlors", sic_code:581203},
     "5": {name:"Gas Stations", sic_code:554101},
     "6": {name:"Hotels", sic_code:701101},
     "7": {name:"Convenience Stores", sic_code:541103},
     "8": {name:"Pharmacy", sic_code:591205},
     "9": {name:"Parking", sic_code:752102},
     "0": {name:"Hospitals", sic_code:806202}
   }
   var url = require('url');
   var url_parts = url.parse(req.url, true);
   var query = url_parts.query;
   var nearbyOptionParam = query.option || "1";
   
   var queryString = {
       key: '24rPdrHSJmUUjBOgD6OU9xDdQxuDcXtu',
       origin: query.origin,
       radius:1,
       ambiguities:'ignore',
       maxMatches:'4',
       hostedData:'mqap.ntpois|group_sic_code=?|'+nearbyOptionsMap[query.option].sic_code
   }
   
   var request = require('request');
     request({url:'http://www.mapquestapi.com/search/v2/radius', qs:queryString}, function (error, response, body) {
         if (!error && response.statusCode == 200) {
           
           res.send(body);
           console.log(body);
         }
         else {
           res.send(error);
           console.log(error);
         }
     })  
});


var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Example app listening at http://%s:%s", host, port)

})