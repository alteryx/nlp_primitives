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
        `nltk's gutenberg corpus. <https://www.nltk.org/book/ch02.html#gutenberg-corpus>`_
        Users can optionally pass in a custom corpus when initializing the primitive
        by specifying the corpus values in a list with the corpus parameter.

        If a string is missing, return `NaN`.

        Note: If a small custom corpus is used, the output of the primitive may vary
        depending on the computer architecture being used (Linux, MacOS, Windows). This
        is especially true when using the default "randomized" algorithm for the
        TruncatedSVD component.

    Args:
        random_seed (int, optional): The random seed value to use for the call to TruncatedSVD.
            Will default to 0 if not specified.
        custom_corpus (list[str], optional): A list of strings to use as a custom corpus. Will
            default to the NLTK Gutenberg corpus if not specified.
        algorithm (str, optional): The algorithm to use for the call to TruncatedSVD. Should be either
            "randomized" or "arpack". Will default to "randomized" if not specified.

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

        Users can optionally also pass in a custom corpus and specify the algorithm to use
        for the TruncatedSVD component used by the primitive.

        >>> custom_corpus = ["dogs ate food", "she ate pineapple", "hello"]
        >>> lsa = LSA(corpus=custom_corpus, algorithm="arpack")
        >>> x = ["The dogs ate food.",
        ...      "She ate a pineapple",
        ...      "Consume Electrolytes, he told me.",
        ...      "Hello",]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.68, 0.78, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """

    name = "lsa"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self, random_seed=0, corpus=None, algorithm="randomized"):
        self.number_output_features = 2
        self.n = 2
        self.trainer = None
        self.random_seed = random_seed
        self.corpus = corpus
        self.algorithm = algorithm
        if self.algorithm not in ["randomized", "arpack"]:
            raise ValueError(
                "TruncatedSVD algorithm must be either 'randomized' or 'arpack'"
            )

    def _create_trainer(self):
        if self.corpus is None:
            gutenberg = nltk.corpus.gutenberg.sents()
            corpus = [" ".join(sent) for sent in gutenberg]
        else:
            corpus = self.corpus
        svd = TruncatedSVD(random_state=self.random_seed, algorithm=self.algorithm)

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

    def get_args_string(self):
        # Override base class method to prevent full custom corpus from being
        # displayed in primitive arguments
        strings = []
        for name, value in self.get_arguments():
            # format arg to string
            if name == "corpus":
                value = "user_defined"
            string = "{}={}".format(name, str(value))
            strings.append(string)

        if len(strings) == 0:
            return ""

        string = ", ".join(strings)
        string = ", " + string
        return string
