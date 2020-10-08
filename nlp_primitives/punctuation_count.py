# -*- coding: utf-8 -*-

import re
import string

import numpy as np
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import NaturalLanguage, Numeric


class PunctuationCount(TransformPrimitive):
    """Determines number of punctuation characters in a string.

    Description:
        Given list of strings, determine the number of punctuation
        characters in each string. Looks for any of the following:

        !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This is a test file.', 'This is second line', 'third line: $1,000']
        >>> punctuation_count = PunctuationCount()
        >>> punctuation_count(x).tolist()
        [1.0, 0.0, 3.0]
    """
    name = "punctuation_count"
    input_types = [NaturalLanguage]
    return_type = Numeric
    default_value = 0

    def get_function(self):
        pattern = "(%s)" % '|'.join([re.escape(x) for x in string.punctuation])

        def punctuation_count(x):
            x = x.reset_index(drop=True)
            counts = x.str.extractall(pattern).groupby(level=0).count()[0]
            counts = counts.reindex_like(x).fillna(0)
            counts[x.isnull()] = np.nan
            return counts.astype(float)
        return punctuation_count
