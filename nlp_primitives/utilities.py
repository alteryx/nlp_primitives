import string
from typing import List

import nltk


def clean_tokens(text: str) -> List[str]:
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = [word.lower() for word in text.split(" ") if len(word) > 0]

    # Remove stopwords and punctuation
    stopwords_and_punctuation = set(nltk.corpus.stopwords.words("english")).union(
        set(string.punctuation),
    )
    text = [word for word in text if word not in stopwords_and_punctuation]

    # Lemmatize tokens
    wn = nltk.WordNetLemmatizer()
    text = [wn.lemmatize(word) for word in text]

    # Set all tokens with a digit in them to '0'
    text = ["0" if any(map(str.isdigit, word)) else word for word in text]
    return text
