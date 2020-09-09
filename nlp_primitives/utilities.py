import os
import string

import nltk

fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../../data/'))
nltk.data.path = [os.path.normpath(os.path.join(fp, 'nltk-data/nltk-data'))]

wn = nltk.WordNetLemmatizer()


def clean_tokens(textstr):
    textstr = textstr.translate(str.maketrans('', '', string.punctuation))
    textstr = [ch for ch in textstr.split(' ') if len(ch) > 0]

    swords = set(nltk.corpus.stopwords.words('english'))
    to_remove = set(string.punctuation).union(swords)
    textstr = [ch.lower() for ch in textstr if ch not in to_remove]

    textstr = [wn.lemmatize(w) for w in textstr]

    textstr = ['0' if any(map(str.isdigit, ch)) else ch for ch in textstr]
    return textstr
