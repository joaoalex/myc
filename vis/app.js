var express = require('express');
var server = express(); // better instead
server.use(express.static(__dirname + '/'));

server.listen(3000);
