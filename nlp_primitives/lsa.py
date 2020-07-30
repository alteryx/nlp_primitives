import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, Pipeline

from .utilities import clean_tokens


class LSA(TransformPrimitive):
    """Calculates the Latent Semantic Analysis Values of Text Input

    Description:
        Given a list of strings, transforms those strings using tf-idf and single
        value decomposition to go from a sparse matrix to a compact matrix with two
        values for each string. These values represent that Latent Semantic Analysis
        of each string. These values will represent their context with respect to
        (nltk's brown sentence corpus.)[https://www.nltk.org/book/ch02.html#brown-corpus].
        Instead of the brown sentence corpus, this primitive may also be passed a
        different LSA pipeline, pre-trained on a different corpus. 

        If a string is missing, return `NaN`.

    Examples:
        >>> lsa = LSA()
        >>> x = ["he helped her walk,", "me me me eat food", "the sentence doth long"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.0, 0.0, 0.01], [0.0, 0.0, 0.0]]

        Now, if we change the values of the input text to something that better resembles
        the brown corpus, the result will be a different, more discerning output. 
        Also, NaN values are handled, as well as strings without words.

        >>> lsa = LSA()
        >>> x = ["the earth is round", "", np.NaN, ".,/"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.01, 0.0, nan, 0.0], [0.0, 0.0, nan, 0.0]]

        If we would rather use a custom corpus, we can use the `make_trainer` function first,
        resulting in a different output for the same input text.

        >>> corpus = ['she will help eat food for a long time', 'I like to walk', 'We go for long walks together']
        >>> trainer = make_trainer(corpus)
        >>> lsa = LSA(trainer=trainer)
        >>> x = ["he helped her walk,", "me me me eat food", "the sentence doth long"]
        >>> res = lsa(x).tolist()
        >>> for i in range(len(res)): res[i] = [abs(round(x, 2)) for x in res[i]]
        >>> res
        [[0.0, 0.34, 0.4], [0.58, 0.0, 0.0]]

    """
    name = "lsa"
    input_types = [Text]
    return_type = Numeric
    default_value = 0

    def __init__(self, trainer=None, random_state=42):
        self.number_output_features = 2
        self.n = 2
        self.random_state = random_state

        if trainer is None:        
            try:
                brown = nltk.corpus.brown.sents()
            except LookupError:
                nltk.download('brown')
                brown = nltk.corpus.brown.sents()
            finally:
                self.trainer = make_pipeline(TfidfVectorizer(), TruncatedSVD(random_state=random_state))
                self.trainer.fit([" ".join(sent) for sent in brown])
        else:
            _validate_trainer(trainer)
            self.trainer = trainer

    def get_function(self):
        dtk = TreebankWordDetokenizer()

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


def _validate_trainer(trainer):
    if not isinstance(trainer, Pipeline):
        raise ValueError('Given LSA pipeline is not a Pipeline object')
    if len(trainer.steps) != 2:
        raise ValueError('Given LSA pipeline contains an incorrect number of transformers')
    if not isinstance(trainer.steps[0][1], TfidfVectorizer):
        raise ValueError('Given LSA pipeline does not have a TfIdfVectorizer as its first transformer')
    if not isinstance(trainer.steps[1][1], TruncatedSVD):
        raise ValueError('Given LSA pipeline does not have a TruncatedSVD as its second transformer')
    try:
        trainer.steps[0][1].vocabulary_
        trainer.steps[1][1].components_
    except AttributeError:
        raise ValueError('Given LSA pipeline should be pre-fitted')


def make_trainer(corpus, random_state=42):
    """ Fits an LSA pipeline with the given corpus which can be used in an LSA primitive

    Arguments:
        corpus (list): A corpus to fit the pipeline with, as a one-dimensional list of strings.
        random_state (int): The random state to seed the TruncatedSVD part of the pipeline with.

    Returns:
        A fitted LSA pipeline object
    """
    trainer = make_pipeline(TfidfVectorizer(), TruncatedSVD(random_state=random_state))
    trainer.fit(corpus)
    return trainer
