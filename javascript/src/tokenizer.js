const language = require('@google-cloud/language');
const { createDocument } = require('./utils');

const client = new language.LanguageServiceClient({
  keyFilename: 'config/auth.json'
});

async function sentTokenize(paragraph) {
  const document = createDocument(paragraph);
  const parsedText = await client.analyzeSyntax({ document });
  return parsedText[0].sentences.map(sentence => sentence.text.content);
}

module.exports = {
  sentTokenize
}