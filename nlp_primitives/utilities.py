import string

import nltk


def clean_tokens(textstr):
    textstr = textstr.translate(str.maketrans("", "", string.punctuation))
    textstr = [word.lower() for word in textstr.split(" ") if len(word) > 0]

    # Remove stopwords and punctuation
    stopwords_and_punctuation = set(nltk.corpus.stopwords.words("english")).union(
        set(string.punctuation)
    )
    textstr = [word for word in textstr if word not in stopwords_and_punctuation]

    # Lemmatize tokens
    wn = nltk.WordNetLemmatizer()
    textstr = [wn.lemmatize(word) for word in textstr]

    # Set all tokens with a digit in them to '0'
    textstr = ["0" if any(map(str.isdigit, word)) else word for word in textstr]
    return textstr
