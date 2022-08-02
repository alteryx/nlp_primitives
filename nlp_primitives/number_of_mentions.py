# -*- coding: utf-8 -*-
import re
import string

import numpy as np
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

from .count_string import CountString


class NumberOfMentions(CountString):
    """Determines the number of mentions in a string.

    Description:
        Given list of strings, determine the number of mentions
        in each string.

        A mention is defined as a string that meets the following criteria:
            - Starts at the start of a string or after whitespace
            - Contains a sequence of word characters
            - Ends with either the end of the string, whitespace, or a non-'@'
              punctuation character
                - e.g. @yes-no IS a valid mention ("#yes")
                - e.g. @yes@ IS NOT a valid mention

        This implementation handles Unicode characters.

        This implementation does not implement any sort of character length limit
        on mentions.

        If a string is missing, return `NaN`.

    Examples:
         >>> x = ['@portland @123oregon456', 'this is a string', '@@@__user1@1and_0@expression']
        >>> number_of_mentions = NumberOfMentions()
        >>> number_of_mentions(x).tolist()
        [2.0, 0.0, 0.0]
    """

    name = "number_of_mentions"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self):
        SPECIALS_MINUS_AT = "".join(list(set(string.punctuation) - {"@"}))
        SPECIALS_MINUS_AT = re.escape(SPECIALS_MINUS_AT)
        pattern = rf"((^@)|(\s+@))(\w+)(?=\s|$|[{SPECIALS_MINUS_AT}])"
        super().__init__(string=pattern, is_regex=True, ignore_case=False)
