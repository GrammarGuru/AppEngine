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
const DIRECT_OBJECT = tags.DIRECT_OBJECT;
const INDIRECT_OBJECT = tags.INDIRECT_OBJECT;
const PREDICATE_NOMINATIVE = tags.PREDICATE_NOMINATIVE;
const PREDICATE_ADJECTIVE = tags.PREDICATE_ADJECTIVE;
const PREPOSITION = tags.PREPOSITION;
const ROOT = tags.ROOT;
const PUNCT = tags.PUNCT;
console.log(POS, tags);

class Parser {
    constructor(tokens) {
        this.words = new Array(tokens.length);
        this.tags = new Array(tokens.length);
        this.dep = new Array(tokens.length);
        this.parents = new Array(tokens.length);
        this.pos = new Array(tokens.length);
        this.children = tokens.map(() => []);
        const self = this;
        let root = null;
        tokens.forEach((item, index) => {
            self.words[index] = item.text.content;
            self.tags[index] = item.partOfSpeech.tag;
            self.dep[index] = item.dependencyEdge.label;
            if(self.dep[index] === 'ROOT')
                root = index;
            self.parents[index] = self.words[item];
            self.children[item.dependencyEdge.headTokenIndex].push(index);
            self.pos[index] = null;
        });
        this.prepCounter = 0;
        this.label(root);
    }

    label(index) {
        const self = this;
        self.pos[index] = POS.Verb;
        self.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(SUBJECTS.has(childDep))
                self.labelNoun(childIndex, POS.Noun);
            else if(VERB_MODIFIERS.has(childDep))
                self.fill(childIndex, POS.Verb, true);
            else if(childDep === DIRECT_OBJECT)
                self.labelNoun(childIndex, POS.DO);
            else if(childDep === INDIRECT_OBJECT)
                self.labelNoun(childIndex, POS.IO);
            else if(childDep === PREDICATE_NOMINATIVE)
                self.labelNoun(childIndex, POS.PN);
            else if(childDep === PREDICATE_ADJECTIVE)
                self.fill(childIndex, POS.PA, true);
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(CLAUSES.has(childDep))
                self.label(childIndex);
        })
    }

    labelNoun(index, tag) {
        this.pos[index] = tag;
        const self = this;
        this.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(NOUN_MODIFIERS.has(childDep))
                self.fill(childIndex, tag);
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(self.isClause(childIndex))
                self.label(childIndex);

        });
    }

    isClause(index) {
        return this.tags[index] === 'Verb' && CLAUSES.has(this.dep[index]);
    }

    labelPrep(index) {
        this.pos[index] = this.prepCounter;
        let tail = undefined;
        const { dep } = this;
        this.children[index].forEach(childIndex => {
            if(dep[childIndex] === PREPOSITION && dep[index] !== PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.labelPrep(childIndex);
        })
        if(tail !== undefined) {
            this.prepCounter++;
            this.labelPrep(tail);
        }
    }

    fill(index, tag, checkPrep=false) {
        this.pos[index] = tag;
        let tail = undefined;
        const { dep } = this;
        this.children[index].forEach(childIndex => {
            if(checkPrep && dep[childIndex] === PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.fill(childIndex, tag, checkPrep);
        })
        if(tail !== undefined) {
            this.prepCounter++;
            this.labelPrep(tail);
        }
    }
}

async function parseLine(text) {
    const document = {
        content: text,
        type: 'PLAIN_TEXT'
    }
    const parsedText = await client.analyzeSyntax({ document });
    const tokens = parsedText[0].tokens;
    const { words, pos } = new Parser(tokens);
    return { words, pos };
}


module.exports = { parseLine };