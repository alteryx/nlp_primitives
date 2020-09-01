import re
import string

import nltk

wn = nltk.WordNetLemmatizer()


def clean_tokens(textstr):
    textstr = textstr.translate(str.maketrans('', '', string.punctuation))
    textstr = [ch for ch in textstr.split(' ') if len(ch)>0]

    try:
        swords = set(nltk.corpus.stopwords.words('english'))
        to_remove = set(string.punctuation).union(swords)
        textstr = [ch.lower() for ch in textstr if ch not in to_remove]
    except LookupError:
        nltk.download('stopwords')
        swords = set(nltk.corpus.stopwords.words('english'))
        to_remove = set(string.punctuation).union(swords)
        textstr = [ch.lower() for ch in textstr if ch not in to_remove]

    try:
        textstr = [wn.lemmatize(w) for w in textstr]
    except LookupError:
        nltk.download('wordnet')
        textstr = [wn.lemmatize(w) for w in textstr]

    finally:
        textstr = ['0' if re.search('[0-9]+', ch) else ch for ch in textstr]
        return textstr
