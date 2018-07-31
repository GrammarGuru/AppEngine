const Parser = require('./parser');
const { sentTokenize } = require('./tokenizer');

async function parse(req, res) {
  try {
    let { line } = req.query;
    let result;
    if (Array.isArray(line)) {
      result = await Promise.all(line.map(l => Parser.parseLine(l)));
    } else {
      result = await Parser.parseLine(line);
    }
    res.send(result);
  } catch (err) {
    res.status(500).send(err);
  }
}

async function filter(req, res) {
  try {
    let { lines } = req.query;
    if(!lines)
      return res.status(400).send('No lines');
    if (!Array.isArray(lines))
      lines = [lines];
    const data = await Promise.all(lines.map(line => Parser.label(line)));
    lines = data.map(d => _filter(d, sentTokenize(d)))
      .filter(line => line.length > 0);
    return res.send(lines);
  } catch (err) {
    res.status(500).send(err);
  }
}

function _isValid({ tokens }, { sentence, root }) {
  if(sentence.includes('(') || sentence.includes(')'))
    return false;
  const parser = new Parser.Parser(tokens, root);
  return parser.isValid();
}

function _filter(data, lines) {
  const result = lines.map(line => _isValid(data, line));
  return lines
    .map(line => line.sentence)
    .filter((_, index) => result[index]);
}

module.exports = { parse, filter }