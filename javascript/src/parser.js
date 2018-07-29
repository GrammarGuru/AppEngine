const language = require('@google-cloud/language');
const POS = require('../config/pos.json');
const tags = require('../config/tags.json');
const { createDocument } = require('./utils');
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
  UNKNOWN,
  EXPLICATIVE
} = tags;


class Parser {
  constructor(tokens, root) {
    this.words = new Array(tokens.length);
    this.tags = new Array(tokens.length);
    this.dep = new Array(tokens.length);
    this.pos = new Array(tokens.length);
    this.children = tokens.map(() => []);
    this.root = root;
    this.prepCounter = 0;
    for (let index = 0; index < tokens.length; index++) {
      const item = tokens[index];
      this.words[index] = item.text.content;
      this.tags[index] = item.partOfSpeech.tag;
      this.dep[index] = item.dependencyEdge.label;
      if (this.dep[index] === 'ROOT' && root === undefined)
        this.root = index;
      if (item.dependencyEdge.headTokenIndex !== index)
        this.children[item.dependencyEdge.headTokenIndex].push(index);
      this.pos[index] = null;
    }
  }

  isValid() {
    const root = this.root;
    return this.tags[root] === 'VERB' &&
      !this.dep.includes(UNKNOWN) &&
      this.children[root].some(childIndex => SUBJECTS.has(this.dep[childIndex]));
  }

  label() {
    this._label(this.root);
  }

  _label(index) {
    this.pos[index] = POS.Verb;
    const isExplicativePhrase = this.isExplicative(index);
    for (const childIndex of this.children[index]) {
      const childDep = this.dep[childIndex];
      if (SUBJECTS.has(childDep)) {
        if(isExplicativePhrase && childDep !== EXPLICATIVE)
          this.labelNoun(childIndex, POS.PN);
        else
          this.labelNoun(childIndex, POS.Noun);
      }
      else if (VERB_MODIFIERS.has(childDep))
        this.fill(childIndex, POS.Verb);
      else if (childDep === DIRECT_OBJECT)
        this.labelNoun(childIndex, POS.DO);
      else if (childDep === INDIRECT_OBJECT)
        this.labelNoun(childIndex, POS.IO);
      else if (childDep === PREDICATE_NOMINATIVE)
        this.labelNoun(childIndex, POS.PN);
      else if (childDep === PREDICATE_ADJECTIVE)
        this.fill(childIndex, POS.PA);
      else if (VERBALS.has(childDep))
        this.labelVerbal(childIndex);
      else if (childDep === PREPOSITION) {
        this.prepCounter++;
        this.labelPrep(childIndex);
      }
      else if (this.isClause(childIndex))
        this._label(childIndex);
    }
  }

  labelNoun(index, tag) {
    this.pos[index] = tag;
    for (const childIndex of this.children[index]) {
      const childDep = this.dep[childIndex];
      if (NOUN_MODIFIERS.has(childDep))
        this.fill(childIndex, tag);
      else if (childDep === APPOS)
        this.labelNoun(childIndex, POS.APPOS);
      else if (VERBALS.has(childDep))
        this.labelVerbal(childIndex);
      else if (childDep === PREPOSITION) {
        this.prepCounter++;
        this.labelPrep(childIndex);
      }
      else if (this.isClause(childIndex))
        this._label(childIndex);
    }
  }

  labelPrep(index) {
    this.pos[index] = this.prepCounter;
    let tails = [];
    for (const childIndex of this.children[index]) {
      const childDep = this.dep[childIndex];
      if (childDep === PREPOSITION)
        tails.push(childIndex)
      else if (CLAUSES.has(childDep))
        this._label(childIndex);
      else if (childDep !== PUNCT)
        this.labelPrep(childIndex);
    }
    tails.forEach(tail => {
      this.prepCounter++;
      this.labelPrep(tail);
    });
  }

  labelVerbal(index, tag) {
    if (!tag) {
      if (this.isInfinitive(index))
        tag = POS.Infinitive;
      else
        tag = POS.Participle;
    }
    this.pos[index] = tag;
    for (const childIndex of this.children[index]) {
      const childDep = this.dep[childIndex];
      if (VERBALS.has(childDep))
        this.labelVerbal(childIndex);
      else if (childDep === PREPOSITION) {
        this.prepCounter++;
        this.labelPrep(childIndex);
      }
      else if (this.dep[childIndex] !== PUNCT)
        this.labelVerbal(childIndex, tag);
    }
  }

  fill(index, tag) {
    this.pos[index] = tag;
    let tail = undefined;
    const {dep} = this;
    for (const childIndex of this.children[index]) {
      if (dep[childIndex] === PREPOSITION)
        tail = childIndex;
      else if (dep[childIndex] !== PUNCT)
        this.fill(childIndex, tag);
    }
    if (tail !== undefined) {
      this.prepCounter++;
      this.labelPrep(tail);
    }
  }

  isClause(index) {
    return this.tags[index] === 'VERB' && CLAUSES.has(this.dep[index]);
  }

  isInfinitive(index) {
    for (const childIndex of this.children[index]) {
      if (this.dep[childIndex] === 'AUX' &&
        this.words[childIndex].toLowerCase() === 'to')
        return true;
    }
    return false;
  }

  isExplicative(index) {
    for (const childIndex of this.children[index]) {
      if(this.dep[childIndex] === EXPLICATIVE)
        return true;
    }
    return false;
  }
}

async function parseLine(text) {
  const parser = await initParser(text);
  parser.label();
  const {words, pos} = parser;
  return {words, pos};
}

async function initParser(text) {
  const parsedText = await label(text);
  const tokens = parsedText.tokens;
  return new Parser(tokens);
}

async function label(text) {
  const document = createDocument(text)
  return (await client.analyzeSyntax({ document }))[0];
}


module.exports = { Parser, parseLine, label};