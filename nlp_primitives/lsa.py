import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from .utilities import clean_tokens


class LSA(TransformPrimitive):
    """Calculates the Latent Semantic Analysis Values of NaturalLanguage Input

    Description:
        Given a list of strings, transforms those strings using tf-idf and single
        value decomposition to go from a sparse matrix to a compact matrix with two
        values for each string. These values represent that Latent Semantic Analysis
        of each string. By default these values will represent their context with respect to
        (nltk's gutenberg corpus.)[https://www.nltk.org/book/ch02.html#gutenberg-corpus].
        Users can optionally pass in a custom corpus when initializing the primitive
        by specifying the corpus values in a list with the corpus parameter.

        If a string is missing, return `NaN`.

    Examples:
        >>> lsa = LSA()
        >>> x = ["he helped her walk,", "me me me eat food", "the sentence doth long"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.01, 0.01, 0.01], [0.0, 0.0, 0.01]]

        Now, if we change the values of the input text, to something that better resembles
        the given corpus, the same given input text will result in a different, more discerning,
        output. Also, NaN values are handled, as well as strings without words.

        >>> lsa = LSA()
        >>> x = ["the earth is round", "", np.NaN, ".,/"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.02, 0.0, nan, 0.0], [0.02, 0.0, nan, 0.0]]
    """

    name = "lsa"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self, random_seed=0, corpus=None):
        self.number_output_features = 2
        self.n = 2
        self.trainer = None
        self.random_seed = random_seed
        self.corpus = corpus

    def _create_trainer(self):
        if self.corpus is None:
            gutenberg = nltk.corpus.gutenberg.sents()
            corpus = [" ".join(sent) for sent in gutenberg]
        else:
            corpus = self.corpus
        svd = TruncatedSVD(random_state=self.random_seed, algorithm="randomized")

        self.trainer = make_pipeline(TfidfVectorizer(), svd)
        self.trainer.fit(corpus)

    def get_function(self):
        if self.trainer is None:
            self._create_trainer()
        dtk = TreebankWordDetokenizer()

        def lsa(array):
            array = pd.Series(array, index=pd.Series(array.index), name="array")
            copy = array.dropna()
            copy = copy.apply(lambda x: dtk.detokenize(clean_tokens(x)))
            li = self.trainer.transform(copy)
            lsa1 = pd.Series(li[:, 0], index=copy.index)
            lsa2 = pd.Series(li[:, 1], index=copy.index)
            array = pd.DataFrame(array)
            array["l1"] = lsa1
            array["l2"] = lsa2

            arr = ((np.array(array[["l1", "l2"]])).T).tolist()
            return pd.Series(arr)

        return lsa
