# -*- coding: utf-8 -*-
import os

import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text

fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../../data/'))
nltk.data.path = [os.path.normpath(os.path.join(fp, 'nltk-data/nltk-data'))]


class StopwordCount(TransformPrimitive):
    """Determines number of stopwords in a string.

    Description:
        Given list of strings, determine the number of stopwords
        characters in each string. Looks for any of the English
        stopwords defined in `nltk.corpus.stopwords`. Case insensitive.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This is a test string.', 'This is second string', 'third string']
        >>> stopword_count = StopwordCount()
        >>> stopword_count(x).tolist()
        [3, 2, 0]
    """
    name = "stopword_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0

    def get_function(self):

        def stopword_count(array):
            li = []
            swords = set(nltk.corpus.stopwords.words('english'))
            tokenizer = nltk.tokenize.word_tokenize
            for el in array:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    words = tokenizer(el)
                    count = len([word for word in words if word.lower() in swords])
                    li.append(count)
            return pd.Series(li)

        return stopword_count
