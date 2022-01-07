import numpy as np
from featuretools.primitives.base import TransformPrimitive
from sklearn.feature_extraction.text import CountVectorizer
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class TokenCount(TransformPrimitive):
    """Calculates the count of each token in the string.

    Description:
        Wrapper function for sklearn.feature_extraction.CountVectorizer.
        https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html

    Example:
        >>> corpus = ['This is the first document.',
        ...           'This document is the second document.',
        ...           'And this is the third one.',
        ...           'Is this the first document?',]
        >>> token_count = TokenCount()
        >>> print(token_count(corpus))
        [[0. 0. 1. 0.]
         [1. 2. 0. 1.]
         [1. 0. 0. 1.]
         [1. 1. 1. 1.]
         [0. 0. 1. 0.]
         [0. 1. 0. 0.]
         [1. 1. 1. 1.]
         [0. 0. 1. 0.]
         [1. 1. 1. 1.]]
        >>> token_count = TokenCount(analyzer='word', ngram_range=(2, 2))
        >>> print(token_count(corpus))
        [[0. 0. 1. 0.]
         [0. 1. 0. 0.]
         [1. 0. 0. 1.]
         [1. 1. 1. 0.]
         [0. 0. 0. 1.]
         [0. 1. 0. 0.]
         [1. 0. 0. 1.]
         [0. 1. 0. 0.]
         [0. 0. 1. 0.]
         [0. 0. 1. 0.]
         [0. 1. 0. 0.]
         [1. 0. 1. 0.]
         [0. 0. 0. 1.]]
    """

    name = "token_count"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={'numeric'})

    def __init__(self, **kwargs):
        self.vectorizer = CountVectorizer(**kwargs)
        self.feature_names = []
        self.number_output_features = 0

    def get_function(self):
        def get_features(column):
            X = self.vectorizer.fit_transform(column.fillna('').to_list())
            self.feature_names = self.vectorizer.get_feature_names_out()
            self.number_output_features = len(self.feature_names)
            X = X.A.astype('float64')
            X[column.isna()] = np.nan
            return X.T
        return get_features

    def generate_names(self, base_feature_names):
        base_name = self.generate_name(base_feature_names)
        return [base_name + "['%s']" % i for i in self.feature_names]
