# -*- coding: utf-8 -*-
from string import punctuation

import pandas as pd
from featuretools.primitives import TransformPrimitive
from nltk import word_tokenize
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class NumberOfWordsInQuotes(TransformPrimitive):
    """Determines the number of words in quotes in a string.

    Description:
        Given a list of strings, determine the number of words in quotes
        in each string.

        This implementation handles Unicode characters.

        If a string is missing, return `NaN`.

    Args:
        quote_type (str, optional): Specify what kind of quotes to match.
        Argument "single" matches on only single quotes (' ').
        Argument "double" matches words between double quotes (" ").
        Argument "both" matches words between either kind of quotes.
        Defaults to "both".

    Examples:
         >>> x = ['"python" java prolog', '"this is a string"', '"binary" "ternary"']
        >>> number_of_words_in_quotes = NumberOfWordsInQuotes()
        >>> number_of_words_in_quotes(x).tolist()
        [1, 4, 2]
    """

    name = "number_of_words_in_quotes"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self, quote_type="both"):
        if quote_type not in ["both", "single", "double"]:
            raise ValueError(
                f"{quote_type} is not a valid quote_type. Specify 'both', 'single', or 'double'"
            )
        self.quote_type = quote_type

    def get_function(self):
        def _word_tokenize(text):
            tokens = word_tokenize(text)
            ct = 0
            for word in tokens:
                if len(word.strip(punctuation).strip()) > 0:
                    ct += 1
            return ct

        def num_words_in_quotes(array):
            IN_DOUBLE_QUOTES = r'"([^"]+)"'
            IN_SINGLE_QUOTES = r"'([^']+)'"
            regex = None
            if self.quote_type == "single":
                regex = IN_SINGLE_QUOTES
            elif self.quote_type == "double":
                regex = IN_DOUBLE_QUOTES
            else:
                regex = f"({IN_SINGLE_QUOTES}|{IN_DOUBLE_QUOTES})"
            text = array.str.extractall(f"{regex}")
            num_words = text[0].apply(_word_tokenize)
            grouped_sum = (
                num_words.groupby(level=0).sum().reindex(array.index, fill_value=pd.NA)
            )
            grouped_sum[grouped_sum.isna()] = 0
            grouped_sum[array.isna()] = pd.NA
            # was defaulting to str type if there are no matches
            return grouped_sum.astype("Int64")

        return num_words_in_quotes
