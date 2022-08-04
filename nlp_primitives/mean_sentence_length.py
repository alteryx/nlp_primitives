# -*- coding: utf-8 -*-
from typing import Iterable

import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from nltk.tokenize import sent_tokenize
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class MeanSentenceLength(TransformPrimitive):
    """Determines mean length of all sentences in a string.

    Description:
        Given list of strings, determine the mean length of all sentences
        in a string.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This.', 'Yay! Yay!', 'String']
        >>> mean_sentence_length = MeanSentenceLength()
        >>> mean_sentence_length(x).tolist()
        [5.0, 4.0, 6.0]
    """

    name = "mean_length_of_sentences"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def get_function(self):
        def helper(text):
            if not isinstance(text, Iterable):
                return np.nan
            if len(text) == 0:
                return 0
            sentences = sent_tokenize(text)
            mean = np.mean([len(s) for s in sentences])
            return mean

        def mean_length_of_sentences(array):
            return array.apply(helper)

        return mean_length_of_sentences
