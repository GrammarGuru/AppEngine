function createDocument(text) {
  return {
    content: text,
    type: 'PLAIN_TEXT'
  }
}

module.exports = {
  createDocument
}