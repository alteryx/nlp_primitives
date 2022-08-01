# -*- coding: utf-8 -*-
import re

import numpy as np
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

from .count_string import CountString


class NumberOfHashtags(CountString):
    """Determines the number of hashtags in a string.

    Description:
        Given list of strings, determine the number of hashtags
        in each string. A hashtag is defined as any word starting
        with a '#' sign followed by a sequence of alphanumeric characters
        or underscores.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['#regular #expression', 'this is a string', '###__regular#1and_0#expression']
        >>> number_of_hashtags = NumberOfHashtags()
        >>> number_of_hashtags(x).tolist()
        [2.0, 0.0, 0.0]
    """

    name = "number_of_hashtags"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def get_function(self):
        pattern = r"#(\w*([^\W\d])+\w*)(?![#\w])"

        def number_of_hashtags(x):
            p = re.compile(pattern)
            x = x.reset_index(drop=True)
            counts = x.str.extractall(p).groupby(level=0).count()[0]
            counts = counts.reindex_like(x).fillna(0)
            counts[x.isnull()] = np.nan
            return counts.astype(float)

        return number_of_hashtags
