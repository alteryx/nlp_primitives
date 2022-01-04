from typing import Iterable

import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

from .constants import common_words_1000


class NumberOfCommonWords(TransformPrimitive):
    """Determines the number of common words in a string.
    Description:
        Given list of strings, determine the number of words that appear in a supplied wordbank.
        The list of strings is case insensitive. The word banks should be all lower case strings.
        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['Hey! This is some natural language', 'bacon, cheesburger, AND, fries', 'I! Am. A; duck?']
        >>> number_of_common_words = NumberOfCommonWords(word_set={'and', 'some', 'am', 'a', 'the', 'is', 'i'})
        >>> number_of_common_words(x).tolist()
        [2, 1, 3]
    """
    name = "number_of_common_words"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={'numeric'})

    default_value = 0

    def __init__(self, word_set=set(common_words_1000), delimiters_regex=r"[- \[\].,!\?;\n]"):
        self.delimiters_regex = delimiters_regex
        self.word_set = word_set

    def get_function(self):
        def get_num_in_word_bank(words):
            if not isinstance(words, Iterable):
                return pd.NA
            num_common_words = 0
            for w in words:
                if w.lower() in self.word_set:  # assumes word_set is all lowercase
                    num_common_words += 1
            return num_common_words

        def num_common_words(x):
            assert (
                self.delimiters_regex is not None
            ), "delimiters_regex needs to be defined"
            assert (
                self.word_set is not None
            ), "word_set needs to be defined"
            words = x.str.split(self.delimiters_regex)
            return words.apply(get_num_in_word_bank)
        return num_common_words
