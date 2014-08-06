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
  database: 'adoptdb'
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

var lastMysqlFetchTimestamp = Date.now();

// listen to the txt file
watch('../isUpdated.txt', function(){

  console.log('last mysql check', lastMysqlFetchTimestamp) ;

  mysql_connection.query('select * from api_adoption where UNIX_TIMESTAMP(`update`) > ' + lastMysqlFetchTimestamp, function(err, rows, fields) {

    console.log(err);

    if (err) throw err;

    lastMysqlFetchTimestamp = Date.now();

    // var rows = [
    //   {
    //     id: 18,
    //     worldid: 'NLD-ZUI',
    //     targetyear: 2015,
    //     user_id: 1,
    //     update: 'Wed Aug 06 2014 18:23:50 GMT+0200 (CEST)',
    //     is_adopted: 1
    //   }
    // ];

    console.log('new data', rows, fields);

    for (var id in sockets) {
      console.log('sending to', id);
      sockets[id].emit('newAdoptions', rows);
    };

  });

});

console.log('Running...');