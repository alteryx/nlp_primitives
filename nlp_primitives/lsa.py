import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from .utilities import clean_tokens


class LSA(TransformPrimitive):
    """Calculates the Latent Semantic Analysis Values of Text Input

    Description:
        Given a list of strings, transforms those strings using tf-idf and single
        value decomposition to go from a sparse matrix to a compact matrix with two
        values for each string. These values represent that Latent Semantic Analysis
        of each string. These values will represent their context with respect to
        the corpus of all strings in the given list.

        If a string is missing, return `NaN`.

    Examples:
        >>> lsa = LSA()
        >>> x = ["he helped her walk,", "me me me eat food", "the sentence doth long"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.0, 0.0, 1.0], [0.0, 1.0, 0.0]]

        NaN values are handled, as well as strings without words.

        >>> lsa = LSA()
        >>> x = ["the earth is round", "", np.NaN, ".,/", "the sun is a star"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[1.0, 0.0, nan, 0.0, 0.0], [0.0, 0.0, nan, 0.0, 1.0]]

    """
    name = "lsa"
    input_types = [Text]
    return_type = Numeric
    default_value = 0

    def __init__(self, random_state=42):
        self.number_output_features = 2
        self.n = 2
        self.random_state = random_state

        self.trainer = make_pipeline(TfidfVectorizer(), TruncatedSVD(random_state=random_state))

    def get_function(self):
        dtk = TreebankWordDetokenizer()

        def lsa(array):
            array = pd.Series(array, index=pd.Series(array.index), name='array')
            copy = array.dropna()
            copy = copy.apply(lambda x: dtk.detokenize(clean_tokens(x)))

            fit_data = copy.tolist()
            # TruncatedSVD cannot produce two features without multiple input values
            if len(fit_data) == 1:
                fit_data = fit_data * 2
            self.trainer.fit(fit_data)

            li = self.trainer.transform(copy)
            lsa1 = pd.Series(li[:, 0], index=copy.index)
            lsa2 = pd.Series(li[:, 1], index=copy.index)
            array = pd.DataFrame(array)
            array['l1'] = lsa1
            array['l2'] = lsa2

            arr = ((np.array(array[['l1', 'l2']])).T).tolist()
            return pd.Series(arr)

        return lsa
