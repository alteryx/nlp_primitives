# -*- coding: utf-8 -*-
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

from .count_string import CountString


class NumberOfHashtags(CountString):
    """Determines the number of hashtags in a string.

    Description:
        Given list of strings, determine the number of hashtags
        in each string.

        A hashtag is defined as a string that meets the following criteria:
            - Starts at the start of a string or after whitespace
            - Contains a sequence of alphanumeric characters
                - The hashtag must contain at least one alphabetic character
            - Ends with either the end of the string, whitespace, or a non-'#'
              punctuation character
                - e.g. #yes-no IS a valid hashtag ("@yes")
                - e.g. #yes# IS NOT a valid hashtag

        This implementation handles Unicode characters.

        This implementation does not implement any sort of character length limit
        on hashtags.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['#regular #expression', 'this is a string', '###__regular#1and_0#expression']
        >>> number_of_hashtags = NumberOfHashtags()
        >>> number_of_hashtags(x).tolist()
        [2, 0, 0]
    """

    name = "number_of_hashtags"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self):
        pattern = r"((^#)|\s#)(\w*([^\W\d])+\w*)(?![#\w])"
        super().__init__(string=pattern, is_regex=True, ignore_case=False)
