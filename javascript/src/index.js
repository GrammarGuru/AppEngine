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
        const result = (await Promise.all(req.body.lines.map(line => Parser.parseLine(line))))
            .filter(result => result !== null);
        res.send(result);
    }
    catch(err) {
        res.status(422).send(err);
    }
}

async function filter(req, res) {
    let { lines } = req.body;
    if(!Array.isArray(lines))
        lines = [lines];
    try {
        const result = await Promise.all(lines.map(line => Parser.isValid(line)));
        res.send(lines.filter((line, index) => {
            return result[index];
        }));
    } catch (err) {
        res.status(422).send(err);
    }
}

module.exports = { parseLine, parseLines, filter }