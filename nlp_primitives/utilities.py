import string

import nltk
import pandas as pd


def clean_tokens(textstr):
    wn = nltk.WordNetLemmatizer()

    textstr = textstr.translate(str.maketrans('', '', string.punctuation))
    textstr = [ch for ch in textstr.split(' ') if len(ch) > 0]

    swords = set(nltk.corpus.stopwords.words('english'))
    to_remove = set(string.punctuation).union(swords)
    textstr = [ch.lower() for ch in textstr if ch not in to_remove]

    textstr = [wn.lemmatize(w) for w in textstr]

    textstr = ['0' if any(map(str.isdigit, ch)) else ch for ch in textstr]
    return textstr


def get_non_empty_tokens(column: pd.Series, regex: str) -> pd.Series:
    tokens = column.str.split(regex)
    non_empty_tokens = tokens.apply(
        lambda x: list(filter(lambda item: item, x)) if isinstance(x, list) else pd.NA
    )
    return non_empty_tokens
