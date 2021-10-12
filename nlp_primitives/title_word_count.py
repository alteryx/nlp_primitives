# -*- coding: utf-8 -*-
import numpy as np
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class TitleWordCount(TransformPrimitive):
    """Determines the number of title words in a string.

    Description:
        Given list of strings, determine the number of title words
        in each string. A title word is defined as any word starting
        with a capital letter. Words at the start of a sentence will
        be counted.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['My favorite movie is Jaws.', 'this is a string', 'AAA']
        >>> title_word_count = TitleWordCount()
        >>> title_word_count(x).tolist()
        [2.0, 0.0, 1.0]
    """
    name = "title_word_count"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})
    default_value = 0

    def get_function(self):
        pattern = r'([A-Z][^\s]*)'

        def title_word_count(x):
            x = x.reset_index(drop=True)
            counts = x.str.extractall(pattern).groupby(level=0).count()[0]
            counts = counts.reindex_like(x).fillna(0)
            counts[x.isnull()] = np.nan
            return counts.astype(float)
        return title_word_count
