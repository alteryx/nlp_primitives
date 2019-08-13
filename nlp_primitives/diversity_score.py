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


class DiversityScore(TransformPrimitive):
    """Calculates the overall complexity of the text based on the total
       number of words used in the text

    Description:
        Given a list of strings, calculates the total number of unique words
        divided by the total number of words in order to give the text a score
        from 0-1 that indicates how unique the words used in it are. This
        primitive only evaluates the 'clean' versions of strings, so ignoring cases,
        punctuation, and stopwords in its evaluation.

        If a string is missing, return `NaN`

    Examples:
        >>> diversity_score = DiversityScore()
        >>> diversity_score(["hi hi hi", "hello its me", "hey what hey what", "a dog ate a basket"]).tolist()
        [0.3333333333333333, 1.0, 0.5, 1.0]
    """
    name = "diversity_score"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = "nltk-data.tar.gz"

    def get_function(self):
        fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
        dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
        nltk.data.path = [os.path.normpath(os.path.join(fp, '../nltk-data/nltk-data'))]
        wn = nltk.WordNetLemmatizer()
        if not os.path.exists(nltk.data.path[0]):
            try:
                tarf = tempfile.mkdtemp()
                if is_python_2():
                    def unpacktar(filename, extract_dir):
                        tarobj = tarfile.open(filename)
                        try:
                            tarobj.extractall(extract_dir)
                        finally:
                            tarobj.close()
                    unpacktar(fp, tarf)
                else:
                    shutil.unpack_archive(fp, tarf)
                shutil.copytree(tarf, dp)
            finally:
                shutil.rmtree(tarf)

        def clean_tokens(textstr):
            textstr = nltk.word_tokenize(textstr)

            processed = [ch.lower() for ch in textstr if ch not in
                         set(string.punctuation).union(
                         set(nltk.corpus.stopwords.words('english')))]
            processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
            processed = [wn.lemmatize(w) for w in processed]
            return processed

        def diversity_score(x):
            li = []
            for el in x:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    el = clean_tokens(el)
                    if len(el) < 1:
                        li.append(0.0)
                    else:
                        li.append(float(len(set(el))) / float(len(el)))
            return pd.Series(li)
        return diversity_score
