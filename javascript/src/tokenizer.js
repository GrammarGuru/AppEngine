function sentTokenize(paragraph) {
  const roots = [];
  for(let i = 0; i < paragraph.tokens.length; i++) {
    const dep = paragraph.tokens[i].dependencyEdge.label;
    if(dep === 'ROOT')
      roots.push(i);
  }
  return paragraph.sentences.map((sentence, index) => ({
    sentence: sentence.text.content,
    root: roots[index]
  }));
}

module.exports = {
  sentTokenize
}