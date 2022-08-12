# -*- coding: utf-8 -*-
import numpy as np
from featuretools.primitives.base import TransformPrimitive
from nltk.tokenize import sent_tokenize
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class MeanCharactersPerSentence(TransformPrimitive):
    """Determines the mean count of characters per sentence in a given string.

    Description:
        Given list of strings, determine the mean count of characters per sentence
        in a string.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This.', 'Yay! Yay!', 'Dog cat.']
        >>> mean_characters_per_sentence = MeanCharactersPerSentence()
        >>> mean_characters_per_sentence(x).tolist()
        [5.0, 4.0, 8.0]
    """

    name = "mean_characters_per_sentence"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def get_function(self):
        def _mean_characters_per_sentence(text):
            if not isinstance(text, str):
                return np.nan
            if len(text) == 0:
                return 0
            sentences = sent_tokenize(text)
            total = 0.0
            for s in sentences:
                total += len(s)
            return total / len(sentences)

        def mean_characters_per_sentence(array):
            return array.apply(_mean_characters_per_sentence)

        return mean_characters_per_sentence
