import nltk, re, pprint
from textblob import TextBlob

def ExtractNP(text):
    nounphrases = []
    words = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(words)
    # print(tagged)
    grammar = r"""
         NP:
            {<DT*|JJ*|JJR*|JJS*>*<NN+><IN>*<NN.*|NNS><CC*>*<NN.*|NNS>.*}
            {<NN+|NNP+|NNS+><IN>*<DT>*<NN.*|NNS>}
            {<NN.*|JJ*>*<NN.*>}
            {<VBG><DT|JJ>*<NN|NNP>}
        """
    chunkParser = nltk.RegexpParser(grammar)
    tree = chunkParser.parse(tagged)
    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        myPhrase = ''
        for item in subtree.leaves():
            myPhrase += ' ' + item[0]
        nounphrases.append(myPhrase.strip())
        # print(myPhrase)
    nounphrases = list(filter(lambda x: len(x.split()) > 1, nounphrases))
    return nounphrases

def ExtractNN(text):
    nouns = []
    blob = TextBlob(text)
    for word, pos in blob.tags:
        if(pos=='NN'):
            nouns.append(word)
    return nouns
# # Evaluation Place
text = 'Briefly, embodiments of a method of classifying a bill are disclosed'
phrases = ExtractNP(text)
print(phrases)
