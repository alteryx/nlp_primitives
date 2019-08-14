import re
import string

import nltk

wn = nltk.WordNetLemmatizer()


def clean_tokens(textstr):
    try:
        swords = set(nltk.corpus.stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        swords = set(nltk.corpus.stopwords.words('english'))
    finally:
        try:
            textstr = nltk.tokenize.word_tokenize(textstr)
        except LookupError:
            nltk.download('punkt')
            textstr = nltk.tokenize.word_tokenize(textstr)
        finally:
            try:
                wn.lemmatize("")
            except LookupError:
                nltk.download('wordnet')
            finally:
                processed = [ch.lower() for ch in textstr if ch not in
                             set(string.punctuation).union(swords)]
                processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
                processed = [wn.lemmatize(w) for w in processed]
                return processed
