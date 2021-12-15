# -*- coding: utf-8 -*-


from typing import Iterable

from featuretools.primitives.base import TransformPrimitive
from numpy import nan
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from nlp_primitives.types import Tokens
from nlp_primitives.utilities import get_non_empty_tokens


def total_length(tokens: Tokens) -> float:
    if not isinstance(tokens, Iterable):
        return nan
    return float(sum(len(x) for x in tokens))


class TotalWordLength(TransformPrimitive):
    """Determines the total word length.

    Description:
        Given list of strings, determine the total
        word length in each string. A word is defined as
        a series of any characters not separated by a delimiter.
        If a string is empty or `NaN`, return `NaN`.

    Examples:
        >>> x = ['This is a test file', 'This is second line', 'third line $1,000']
        >>> total_word_length = TotalWordLength()
        >>> total_word_length(x).tolist()
        [15.0, 16.0, 15.0]
    """
    name = "total_word_length"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})
    default_value = 0

    def __init__(self, delimiters_regex=None):
        self.delimiters_regex = delimiters_regex

    def get_function(self):
        def total_word_length(x):
            x = get_non_empty_tokens(x, regex=self.delimiters_regex)
            return x.apply(total_length)
        return total_word_length
