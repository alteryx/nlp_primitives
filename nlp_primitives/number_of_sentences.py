# -*- coding: utf-8 -*-
import numpy as np
from featuretools.primitives.base import TransformPrimitive
from nltk.tokenize import sent_tokenize
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class NumberOfSentences(TransformPrimitive):
    """Determines number of sentences in a string.

    Description:
        Given list of strings, determine the number of sentences
        in each string.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This is a test string.', 'This is second string! This is a second string', 'third string.']
        >>> number_of_sentences = NumberOfSentences()
        >>> number_of_sentences(x).tolist()
        [1, 2, 1]
    """

    name = "number_of_sentences"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})
    default_value = 0

    def get_function(self):
        def _number_of_sentences(text):
            if not isinstance(text, str):
                return np.nan
            if len(text) == 0:
                return 0
            sentences = sent_tokenize(text)
            return len(sentences)

        def number_of_sentences(array):
            return array.apply(_number_of_sentences)

        return number_of_sentences
