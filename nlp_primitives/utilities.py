import string

import nltk


def clean_tokens(textstr):
    textstr = textstr.translate(str.maketrans("", "", string.punctuation))
    textstr = [ch.lower() for ch in textstr.split(" ") if len(ch) > 0]

    # Remove stopwords and punctuation
    stopwords_and_punctuation = set(nltk.corpus.stopwords.words("english")).union(
        set(string.punctuation)
    )
    textstr = [ch for ch in textstr if ch not in stopwords_and_punctuation]

    # Lemmatize tokens
    wn = nltk.WordNetLemmatizer()
    textstr = [wn.lemmatize(w) for w in textstr]

    # Set all tokens with a digit in them to '0'
    textstr = ["0" if any(map(str.isdigit, ch)) else ch for ch in textstr]
    return textstr
