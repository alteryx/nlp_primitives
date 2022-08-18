# -*- coding: utf-8 -*-
import re
from string import punctuation

import pandas as pd
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

    Args:
        quote_type (str, optional): Specify what kind of quotes to match.
        Argument "single" matches on only single quotes (' ').
        Argument "double" matches words between double quotes (" ").
        Argument "both" matches words between either kind of quotes.
        Defaults to "both".

    Examples:
         >>> x = ['"python" java prolog "Diffie-Hellman"', '"this is a string user@email"', '"binary" "ternary" "wikipedia.org"']
        >>> number_of_words_in_quotes = NumberOfWordsInQuotes()
        >>> number_of_words_in_quotes(x).tolist()
        [2, 5, 3]
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
        IN_DOUBLE_QUOTES = r'"[^"]+"'
        IN_SINGLE_QUOTES = r"'[^']+'"
        if quote_type == "double":
            self.regex = IN_DOUBLE_QUOTES
        elif quote_type == "single":
            self.regex = IN_SINGLE_QUOTES
        else:
            self.regex = f"({IN_SINGLE_QUOTES}|{IN_DOUBLE_QUOTES})"
        self.DELIMITERS = set(punctuation) - {'"', ".", "'", "-", ":", "@", "/", "\\"}
        self.DELIMITERS = "".join(list(self.DELIMITERS))
        self.DELIMITERS = re.escape(f" {self.DELIMITERS}\n\t")

    def get_function(self):
        def count_words_in_quotes(text):
            if pd.isnull(text):
                return pd.NA
            matches = re.findall(self.regex, text)
            ct = 0
            for match in matches:
                words = re.split(f"[{self.DELIMITERS}]", match)
                for word in words:
                    print(f"Word: {word}")
                    if len(word.strip(punctuation + " ")):
                        ct += 1
            return ct

        def num_words_in_quotes(array):
            return array.apply(count_words_in_quotes).astype("Int64")

        return num_words_in_quotes
