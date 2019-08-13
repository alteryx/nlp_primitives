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
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline


class LSA(TransformPrimitive):
    """Calculates the Latent Semantic Analysis Values of Text Input

    Description:
        Given a list of strings, transforms those strings using tf-idf and single
        value decomposition to go from a sparse matrix to a compact matrix with two
        values for each string. These values represent that Latent Semantic Analysis
        of each string. These values will represent their context with respect to
        (nltk's brown sentence corpus.)[https://www.nltk.org/book/ch02.html#brown-corpus]

        If a string is missing, return `NaN`.

    Examples:
        >>> lsa = LSA()
        >>> x = ["he helped her walk,", "me me me eat food", "the sentence doth long"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.0, 0.0, 0.01], [0.0, 0.0, 0.0]]

        Now, if we change the values of the input corpus, to something that better resembles
        the given text, the same given input text will result in a different, more discerning,
        output. Also, NaN values are handled, as well as strings without words.

        >>> lsa = LSA()
        >>> x = ["the earth is round", "", np.NaN, ".,/"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.01, 0.0, nan, 0.0], [0.0, 0.0, nan, 0.0]]

    """
    name = "lsa"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = "nltk-data.tar.gz"

    def __init__(self):
        # TODO: allow user to use own corpus
        self.number_output_features = 2
        self.n = 2

        fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
        dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
        data_path = os.path.normpath(os.path.join(fp, '../nltk-data/nltk-data'))
        nltk.data.path.append(data_path)

        if not os.path.exists(data_path):
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
        sents_list = [" ".join(sent) for sent in nltk.corpus.brown.sents()]

        self.trainer = make_pipeline(TfidfVectorizer(), TruncatedSVD())
        self.trainer.fit(sents_list)

    def get_function(self):
        dtk = TreebankWordDetokenizer()
        wn = nltk.WordNetLemmatizer()

        def clean_tokens(textstr):
            textstr = nltk.word_tokenize(textstr)

            processed = [ch.lower() for ch in textstr if ch not in
                         set(string.punctuation).union(
                         set(nltk.corpus.stopwords.words('english')))]
            processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
            processed = [wn.lemmatize(w) for w in processed]
            return processed

        def lsa(array):
            array = pd.Series(array, index=pd.Series(array.index), name='array')
            copy = array.dropna()
            copy = copy.apply(lambda x: dtk.detokenize(clean_tokens(x)))
            li = self.trainer.transform(copy)
            lsa1 = pd.Series(li[:, 0], index=copy.index)
            lsa2 = pd.Series(li[:, 1], index=copy.index)
            array = pd.DataFrame(array)
            array['l1'] = lsa1
            array['l2'] = lsa2

            arr = ((np.array(array[['l1', 'l2']])).T).tolist()
            return pd.Series(arr)

        return lsa
