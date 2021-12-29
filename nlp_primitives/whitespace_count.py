# -*- coding: utf-8 -*-
import numpy as np
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class StringCount(TransformPrimitive):
    """pd.Series.str.count"""

    name = "string_count"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={'numeric'})

    def __init__(self, regex=None):
        self.regex = regex

    def get_function(self):
        def get_str_count(column):
            assert self.regex is not None, "regex needs to be defined"
            return column.str.count(self.regex)

        return get_str_count


class WhitespaceCount(StringCount):
    """Calculates number of whitespaces in a string.

    Description:
        Given a list of strings, determine the whitespaces in each string
        If a string is missing, return `NaN`

    Examples:
        >>> x = ['', 'hi im ethan', 'multiple    spaces']
        >>> upper_case_count = WhitespaceCount()
        >>> upper_case_count(x).tolist()
        [0, 2, 4]
    """

    name = "whitespace_count"
    default_value = 0

    def __init__(self):
        super().__init__(" ")
