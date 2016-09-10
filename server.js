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
   console.log("Got a GET request for /list_user");
   var url = require('url');
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;
    var params = query.src+"\n"+query.dest;

    fs.writeFile( __dirname + "/public/" + "location.js", params, function(err) {
        if(err) {
            return console.log(err);
        }

        console.log("The file was saved!");
    }); 
    fs.readFile( __dirname + "/public/" + "index.html", 'utf8', function (err, data) {
        console.log( data );
        // setTimeout(function(){
          webshot(data, 'map.png', {siteType:'html'}, function(err) {
            // screenshot now saved to google.png
          });
        // }, 20000);

        
        res.send( data );
     });
})



var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("Example app listening at http://%s:%s", host, port)

})