# -*- coding: utf-8 -*-

import re

import numpy as np
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text


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
        [3.0, 2.0, 0.0]
    """
    name = "stopword_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = "english_stopwords.txt"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        with open(file_path, 'r') as f:
            stopwords = [line.strip() for line in f]
        escaped_stopwords = [re.escape(x) for x in stopwords]
        pattern = '(%s)' % '|'.join([r'\b%s\b' % x for x in escaped_stopwords])

        def stopword_count(x):
            x = x.reset_index(drop=True)
            counts = x.str.lower().str.extractall(pattern).groupby(level=0).count()[0]
            counts = counts.reindex_like(x).fillna(0)
            counts[x.isnull()] = np.nan
            return counts.astype(float)
        return stopword_count
