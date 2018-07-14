// Imports the Google Cloud client library
const language = require('@google-cloud/language');
const POS = require('../config/pos.json');
const tags = require('../config/tags.json');
// Instantiates a client
const client = new language.LanguageServiceClient({
    keyFilename: 'config/auth.json'
});


const NOUN_MODIFIERS = new Set(tags.NOUN_MODIFIERS);
const VERB_MODIFIERS = new Set(tags.VERB_MODIFIERS);
const SUBJECTS = new Set(tags.SUBJECTS);
const CLAUSES = new Set(tags.CLAUSES);
const VERBALS = new Set(tags.VERBALS);
const {
    DIRECT_OBJECT,
    INDIRECT_OBJECT,
    PREDICATE_NOMINATIVE,
    PREDICATE_ADJECTIVE,
    PREPOSITION,
    ROOT,
    PUNCT,
    APPOS,
    UNKNOWN
} = tags;


class Parser {
    constructor(tokens) {
        this.words = new Array(tokens.length);
        this.tags = new Array(tokens.length);
        this.dep = new Array(tokens.length);
        this.pos = new Array(tokens.length);
        this.children = tokens.map(() => []);
        this.roots = [];
        const self = this;
        tokens.forEach((item, index) => {
            self.words[index] = item.text.content;
            self.tags[index] = item.partOfSpeech.tag;
            self.dep[index] = item.dependencyEdge.label;
            if(self.dep[index] === 'ROOT')
                self.roots.push(index);
            if(item.dependencyEdge.headTokenIndex !== index)
                self.children[item.dependencyEdge.headTokenIndex].push(index);
            self.pos[index] = null;
        });
        this.prepCounter = 0;
    }

    isValid() {
        const root = this.roots[0];
        return this.tags[root] === 'VERB' &&
            !this.dep.includes(UNKNOWN) &&
            this.children[root].some(childIndex => {
                return SUBJECTS.has(this.dep[childIndex])
            });
    }

    label() {
        this.roots.forEach(root => this._label(root));
    }

    _label(index) {
        this.pos[index] = POS.Verb;
        for(const childIndex of this.children[index]) {
            const childDep = this.dep[childIndex];
            if(SUBJECTS.has(childDep))
                this.labelNoun(childIndex, POS.Noun);
            else if(VERB_MODIFIERS.has(childDep))
                this.fill(childIndex, POS.Verb);
            else if(childDep === DIRECT_OBJECT)
                this.labelNoun(childIndex, POS.DO);
            else if(childDep === INDIRECT_OBJECT)
                this.labelNoun(childIndex, POS.IO);
            else if(childDep === PREDICATE_NOMINATIVE)
                this.labelNoun(childIndex, POS.PN);
            else if(childDep === PREDICATE_ADJECTIVE)
                this.fill(childIndex, POS.PA);
            else if(VERBALS.has(childDep))
                this.labelVerbal(childIndex);
            else if(childDep === PREPOSITION) {
                this.prepCounter++;
                this.labelPrep(childIndex);
            }
            else if(this.isClause(childIndex))
                this._label(childIndex);
        }
    }

    labelNoun(index, tag) {
        this.pos[index] = tag;
        for(const childIndex of this.children[index]) {
            const childDep = this.dep[childIndex];
            if(NOUN_MODIFIERS.has(childDep))
                this.fill(childIndex, tag);
            else if(childDep === APPOS)
                this.labelNoun(childIndex, POS.APPOS);
            else if(VERBALS.has(childDep))
                this.labelVerbal(childIndex);
            else if(childDep === PREPOSITION) {
                this.prepCounter++;
                this.labelPrep(childIndex);
            }
            else if(this.isClause(childIndex))
                this.label(childIndex);
        }
    }

    labelPrep(index) {
        this.pos[index] = this.prepCounter;
        let tails = [];
        for(const childIndex of this.children[index]) {
            const childDep = self.dep[childIndex];
            if(childDep === PREPOSITION)
                tails.push(childIndex)
            else if(CLAUSES.has(childDep))
                this.label(childIndex);
            else if(childDep !== PUNCT)
                this.labelPrep(childIndex);
        }
        tails.forEach(tail => {
            this.prepCounter++;
            this.labelPrep(tail);
        });
    }

    labelVerbal(index, tag) {
        if(!tag) {
            if(this.isInfinitive(index))
                tag = POS.Infinitive;
            else
                tag = POS.Participle;
        }
        this.pos[index] = tag;
        for(const childIndex of this.children[index]) {
            const childDep = this.dep[childIndex];
            if(VERBALS.has(childDep))
                this.labelVerbal(childIndex);
            else if(childDep === PREPOSITION) {
                this.prepCounter++;
                this.labelPrep(childIndex);
            }
            else if(this.dep[childIndex] !== PUNCT)
                this.labelVerbal(childIndex, tag);
        }
    }

    fill(index, tag) {
        this.pos[index] = tag;
        let tail = undefined;
        const { dep } = this;
        for(const childIndex of this.children[index]) {
            if(dep[childIndex] === PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.fill(childIndex, tag);
        }
        if(tail !== undefined) {
            this.prepCounter++;
            this.labelPrep(tail);
        }
    }

    isClause(index) {
        return this.tags[index] === 'VERB' && CLAUSES.has(this.dep[index]);
    }

    isInfinitive(index) {
        for(const childIndex of this.children[index]) {
            if (this.dep[childIndex] === 'AUX' &&
                this.words[childIndex].toLowerCase() === 'to')
                return true;
        }
        return false;
    }
}

async function parseLine(text) {
    const parser = await initParser(text);
    parser.label();
    const { words, pos } = parser;
    return { words, pos };
}

async function isValid(text) {
    const parser = await initParser(text);
    return parser.isValid();
}

async function initParser(text) {
    const document = createDocument(text)
    const parsedText = await client.analyzeSyntax({ document });
    const tokens = parsedText[0].tokens;
    return new Parser(tokens);
}

function createDocument(text) {
    return {
        content: text,
        type: 'PLAIN_TEXT'
    }
}


module.exports = { parseLine, isValid };