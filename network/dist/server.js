const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, '.')));

app.get('/*', function (req, res) {
  res.sendFile(path.join(__dirname, '.', 'index.html'));
});

const port = 8888;
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

