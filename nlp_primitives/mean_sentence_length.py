# -*- coding: utf-8 -*-
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
        >>> x = ['This is a test string.', 'This is second string! This is a second string', 'third string']
        >>> mean_sentence_length = MeanSentenceLength()
        >>> mean_sentence_length(x).tolist()
        [1.0, 2.0, 0.0]
    """

    name = "mean_length_of_sentences"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def get_function(self):
        def mean_length_of_sentences(text):
            ans = []
            for t in text:
                if pd.isna(t):
                    ans.append(np.nan)
                else:
                    if len(t) == 0:
                        ans.append(0)
                    else:
                        sentences = sent_tokenize(t)
                        mean = np.mean([len(s) for s in sentences])
                        ans.append(mean)
            return pd.Series(ans)

        return mean_length_of_sentences
