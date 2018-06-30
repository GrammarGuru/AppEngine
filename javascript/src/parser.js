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
const {
    DIRECT_OBJECT,
    INDIRECT_OBJECT,
    PREDICATE_NOMINATIVE,
    PREDICATE_ADJECTIVE,
    PREPOSITION,
    ROOT,
    PUNCT,
    APPOS,
    PARTICIPLE,
    INF
} = tags;


class Parser {
    constructor(tokens) {
        this.words = new Array(tokens.length);
        this.tags = new Array(tokens.length);
        this.dep = new Array(tokens.length);
        this.parents = new Array(tokens.length);
        this.pos = new Array(tokens.length);
        this.children = tokens.map(() => []);
        const self = this;
        let roots = [];
        tokens.forEach((item, index) => {
            self.words[index] = item.text.content;
            self.tags[index] = item.partOfSpeech.tag;
            self.dep[index] = item.dependencyEdge.label;
            if(self.dep[index] === 'ROOT')
                roots.push(index);
            self.parents[index] = self.words[item];
            self.children[item.dependencyEdge.headTokenIndex].push(index);
            self.pos[index] = null;
        });
        this.prepCounter = 0;
        roots.forEach(root => this.label(root));
    }

    label(index) {
        const self = this;
        self.pos[index] = POS.Verb;
        self.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(SUBJECTS.has(childDep))
                self.labelNoun(childIndex, POS.Noun);
            else if(VERB_MODIFIERS.has(childDep))
                self.fill(childIndex, POS.Verb);
            else if(childDep === DIRECT_OBJECT)
                self.labelNoun(childIndex, POS.DO);
            else if(childDep === INDIRECT_OBJECT)
                self.labelNoun(childIndex, POS.IO);
            else if(childDep === PREDICATE_NOMINATIVE)
                self.labelNoun(childIndex, POS.PN);
            else if(childDep === PREDICATE_ADJECTIVE)
                self.fill(childIndex, POS.PA);
            else if(childDep === PARTICIPLE)
                self.fill(childIndex, POS.PARTICIPLE);
            else if(self.isInfinitive(childIndex)) {
                self.fill(childIndex, POS.Infinitive);
            }
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(self.isClause(childIndex))
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
            else if(childDep === APPOS)
                self.labelNoun(childIndex, POS.APPOS);
            else if(childDep === PREPOSITION) {
                self.prepCounter++;
                self.labelPrep(childIndex);
            }
            else if(self.isClause(childIndex))
                self.label(childIndex);

        });
    }

    isClause(index) {
        return this.tags[index] === 'VERB' && CLAUSES.has(this.dep[index]);
    }

    isInfinitive(index) {
        return this.tags[index] === 'VERB' && this.dep[index] === INF;
    }

    labelPrep(index) {
        console.log(index, this.words[index]);
        this.pos[index] = this.prepCounter;
        let tails = [];
        const self = this;
        this.children[index].forEach(childIndex => {
            const childDep = self.dep[childIndex];
            if(childDep === PREPOSITION)
                tails.push(childIndex)
            else if(CLAUSES.has(childDep))
                self.label(childIndex);
            else if(childDep !== PUNCT)
                this.labelPrep(childIndex);
        })
        tails.forEach(tail => {
            this.prepCounter++;
            this.labelPrep(tail);
        });
    }

    fill(index, tag) {
        this.pos[index] = tag;
        let tail = undefined;
        const { dep } = this;
        this.children[index].forEach(childIndex => {
            if(dep[childIndex] === PREPOSITION)
                tail = childIndex;
            else if(dep[childIndex] !== PUNCT)
                this.fill(childIndex, tag);
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