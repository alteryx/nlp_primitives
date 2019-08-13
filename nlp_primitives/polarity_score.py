import os
import re
import shutil
import string
import tarfile
import tempfile

import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.utils import is_python_2
from featuretools.variable_types import Numeric, Text
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer


class PolarityScore(TransformPrimitive):
    """Calculates the polarity of a text on a scale from -1 (negative) to 1 (positive)

    Description:
        Given a list of strings assign a polarity score from -1 (negative text),
        to 0 (neutral text), to 1 (positive text). The functions returns a score
        for every given piece of text. If a string is missing, return 'NaN'

    Examples:
        >>> x = ['He loves dogs', 'She hates cats', 'There is a dog', '']
        >>> polarity_score = PolarityScore()
        >>> polarity_score(x).tolist()
        [0.677, -0.649, 0.0, 0.0]
    """
    name = "polarity_score"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = 'nltk-data.tar.gz'

    def get_function(self):
        dtk = TreebankWordDetokenizer()
        wn = nltk.WordNetLemmatizer()

        fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
        dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
        nltk.data.path = [os.path.normpath(os.path.join(fp, '../nltk-data/nltk-data'))]
        if not os.path.exists(nltk.data.path[0]):
            try:
                tf = tempfile.mkdtemp()
                if is_python_2():
                    def unpacktar(filename, extract_dir):
                        tarobj = tarfile.open(filename)
                        try:
                            tarobj.extractall(extract_dir)
                        finally:
                            tarobj.close()
                    unpacktar(fp, tf)
                else:
                    shutil.unpack_archive(fp, tf)
                shutil.copytree(tf, dp)
            finally:
                shutil.rmtree(tf)

        def clean_tokens(textstr):
            textstr = nltk.word_tokenize(textstr)

            processed = [ch.lower() for ch in textstr if ch not in
                         set(string.punctuation).union(
                         set(nltk.corpus.stopwords.words('english')))]
            processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
            processed = [wn.lemmatize(w) for w in processed]
            return processed

        def polarity_score(x):
            vader = SentimentIntensityAnalyzer()
            li = []

            def vader_pol(sentence):
                return (vader.polarity_scores(sentence)['pos'] -
                        vader.polarity_scores(sentence)['neg'])
            for el in x:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    el = clean_tokens(el)
                    if len(el) < 1:
                        li.append(0.0)
                    else:
                        li.append(vader_pol(dtk.detokenize(el)))
            return pd.Series(li)
        return polarity_score
