import re
import string

import nltk

wn = nltk.WordNetLemmatizer()


def clean_tokens(textstr):
    try:
        textstr = nltk.tokenize.word_tokenize(textstr)
    except LookupError:
        nltk.download('punkt')
        textstr = nltk.tokenize.word_tokenize(textstr)

    try:
        swords = set(nltk.corpus.stopwords.words('english'))
        textstr = [ch.lower() for ch in textstr if ch not in tset(string.punctuation).union(swords)]
    except LookupError:
        nltk.download('stopwords')
        swords = set(nltk.corpus.stopwords.words('english'))
        textstr = [ch.lower() for ch in textstr if ch not in set(string.punctuation).union(swords)]

    try:
        textstr = [wn.lemmatize(w) for w in textstr]
    except LookupError:
        nltk.download('wordnet')
        textstr = [wn.lemmatize(w) for w in textstr]

    finally:
        textstr = ['0' if re.search('[0-9]+', ch) else ch for ch in textstr]
        return textstr
