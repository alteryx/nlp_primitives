import shutil
import string
import tempfile
from pathlib import Path

import nltk


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


def unpack_data():
    if not Path(nltk.data.path[0]).exists():
        fp = (Path(__file__) / '../../data/nltk-data.tar.gz').resolve()
        dp = (fp / '../nltk-data').resolve()
        nltk.data.path.append(dp / 'nltk-data')
        try:
            tf = tempfile.mkdtemp()
            shutil.unpack_archive(fp, tf)
            if dp.exists():
                shutil.rmtree(dp)
            shutil.copytree(tf, dp)
            print('Unloaded nltk data to', dp)
        finally:
            shutil.rmtree(tf)


unpack_data()
