var app = require('http').createServer(function(req, res){
  res.writeHead(302, {
    'Location': '/'
  });
  res.end();
});

var io = require('socket.io')(app);
var fs = require('fs');
var watch = require('node-watch');

var mysql = require('mysql');
var mysql_connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'adoptdb',
});

var sockets = {} ;

app.listen(4000);

io.on('connect', function (socket) {

  console.log('connect!', socket.id);
  sockets[socket.id] = socket ;

  socket.on('disconnect', function(){

    console.log('disconnect!', socket.id);
    delete sockets[socket.id];

  });

});

mysql_connection.connect();

var getMysqlFriendlyTimestamp = function(){

  var date = new Date();
  return date.getUTCFullYear() + '-' +
    ('00' + (date.getUTCMonth()+1)).slice(-2) + '-' +
    ('00' + date.getUTCDate()).slice(-2) + ' ' + 
    ('00' + date.getUTCHours()).slice(-2) + ':' + 
    ('00' + date.getUTCMinutes()).slice(-2) + ':' + 
    ('00' + date.getUTCSeconds()).slice(-2);

}

var lastMysqlFetchTimestamp = getMysqlFriendlyTimestamp();

// listen to the txt file
watch('../isUpdated.txt', function(){

  console.log('last mysql check', lastMysqlFetchTimestamp) ;

  mysql_connection.query('select * from api_adoption where `update` > ?', lastMysqlFetchTimestamp, function(err, rows, fields) {

    console.log(err);

    if (err) throw err;

    lastMysqlFetchTimestamp = getMysqlFriendlyTimestamp();

    console.log('new data', rows.length);

    //for testing purposes
    rows = [
      {
        id: 45,
        is_adopted: 1,
        oz_country_name: "iran",
        oz_zone_name: "yolo",
        targetyear: 2015,
        update: "2014-08-15T11:02:56.000Z",
        user_display_name: "joshua",
        user_id: 1,
        worldid: "PHL-CEL-ZAM",
      },
      {
        id: 45,
        is_adopted: 1,
        oz_country_name: "philipines",
        oz_zone_name: "yolo",
        targetyear: 2020,
        update: "2014-08-15T11:02:56.000Z",
        user_display_name: "joshua",
        user_id: 1,
        worldid: "PHL-CEL-NUE",
      },
      {
        id: 45,
        is_adopted: 1,
        oz_country_name: "belgium",
        oz_zone_name: "yolo",
        targetyear: 2015,
        update: "2014-08-15T11:02:56.000Z",
        user_display_name: "joshua",
        user_id: 1,
        worldid: "PHL-CEL-BAT",
      }
    ] ;

    for (var id in sockets) {
      console.log('sending to', id);
      sockets[id].emit('newAdoptions', rows);
    };

  });

});

console.log('Running...');