const express = require('express');
const bodyParser = require('body-parser');
const { parse, filter } = require('./src');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/labels', parse);
app.post('/filter', filter);

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});