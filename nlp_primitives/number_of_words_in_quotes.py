# -*- coding: utf-8 -*-
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

from .count_string import CountString


class NumberOfWordsInQuotes(TransformPrimitive):
    """Determines the number of words in quotes in a string.

    Description:
        Given a list of strings, determine the number of words enclosed in quotation marks (" or ')
        in each string. Includes argument options to

        This primitive handles Unicode characters.

    Args:
        double_only (bool, optional): Only count words enclosed in double quotation marks ("")
        Defaults to False.

        single_only (bool, optional): Only count words enclosed in single quotation marks ('')
        Defaults to False.

    Examples:
        >>> x = ['"original"', '"this is a string"', "'single quotes'"]
        >>> number_of_words_in_quotes = NumberOfWordsInQuotes()
        >>> number_of_words_in_quotes(x).tolist()
        [1.0, 4.0, 2.0]
    """

    name = "number_of_words_in_quotes"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self, double_only=False, single_only=False):
        if double_only and single_only:
            raise Exception
        self.double_only = double_only
        self.single_only = single_only

    def get_function():
        def num_words_in_quotes(array):
            ans = array.str.extractall('"(\w+[^"]*)+"')
            return len(ans)

        return num_words_in_quotes
