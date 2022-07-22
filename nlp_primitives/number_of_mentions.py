# -*- coding: utf-8 -*-
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from .count_string import CountString


class NumberOfMentions(CountString):
    """Determines the number of mentions in a string.

    Description:
        Given list of strings, determine the number of mentions
        in each string. A mention is defined as any word starting
        with a '@' sign followed by a sequence of alphanumeric characters
        or underscores.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['#regular#expression', 'this is a string', '###__regular#1and_0#expression']
        >>> number_of_mentions = NumberOfmentions()
        >>> number_of_mentions(x).tolist()
        [2.0, 0.0, 3.0]
    """

    name = "number_of_mentions"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self):
        pattern = r"(@[A-Za-z0-9|\_]+)"
        return super().__init__(string=pattern, is_regex=True)
