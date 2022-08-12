# -*- coding: utf-8 -*-
import re
import string

from featuretools.primitives import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class NumberOfWordsInQuotes(TransformPrimitive):
    """Determines the number of words in quotes in a string.

    Description:
        Given a list of strings, determine the number of words in quotes
        in each string.

        This implementation handles Unicode characters.

        If a string is missing, return `NaN`.

    Examples:
         >>> x = ['"yes" I said', '"this is a string"', '"yep" "nope"']
        >>> number_of_words_in_quotes = NumberOfWordsInQuotes()
        >>> number_of_words_in_quotes(x).tolist()
        [1.0, 4.0, 2.0]
    """

    name = "number_of_words_in_quotes"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self, arg=None):
        pass

    def get_function(self):
        def num_words_in_quotes(array):
            text = array.str.extractall(r"\"([^\"]+)\"")
            assert 0
            return text

        return num_words_in_quotes
