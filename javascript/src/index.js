const Parser = require('./parser');

async function parseLine(req, res) {
    try{
        const result = await Parser.parseLine(req.body.line);
        res.send(result);
    }
    catch(err) {
        res.status(422).send(err);
    }
}

async function parseLines(req, res) {
    try {
        const result = await Promise.all(req.body.lines.map(line => Parser.parseLine(line)));
        res.send(result);
    }
    catch(err) {
        res.status(422).send(err);
    }
}

module.exports = { parseLine, parseLines }