const Parser = require('./parser');
const { sentTokenize } = require('./tokenizer');

async function parseLine(req, res) {
  const result = await Parser.parseLine(req.body.line);
  res.send(result);
}

async function parseLines(req, res) {
  let { lines } = req.body;
  if (!Array.isArray(lines))
    lines = [lines];
  const result = await Promise.all(lines.map(line => Parser.parseLine(line)));
  res.send(result);
}

async function filter(req, res) {
  let { lines } = req.body;
  if(!lines)
    return res.status(400).send('No lines');
  if (!Array.isArray(lines))
    lines = [lines];
  lines = await Promise.all(lines.map(line => sentTokenize(line)));
  let result = await Promise.all(lines.map(paragraph => _filter(paragraph)));
  for(let index = 0; index < result.length; index++) {
    if(lines[index])
      lines[index] = lines[index].filter((_, subIndex) => result[index][subIndex])
    if(!lines[index] || lines[index].length === 0)
      lines.splice(index, 1);
  }
  return res.send(lines);
}

async function _filter(lines) {
  return Promise.all(lines.map(line => Parser.isValid(line)));
}

module.exports = { parseLine, parseLines, filter }