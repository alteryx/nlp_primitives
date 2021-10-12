# -*- coding: utf-8 -*-

import re

from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class MeanCharactersPerWord(TransformPrimitive):
    """Determines the mean number of characters per word.

    Description:
        Given list of strings, determine the mean number of
        characters per word in each string. A word is defined as
        a series of any characters not separated by white space.
        Punctuation is removed before counting. If a string
        is empty or `NaN`, return `NaN`.

    Examples:
        >>> x = ['This is a test file', 'This is second line', 'third line $1,000']
        >>> mean_characters_per_word = MeanCharactersPerWord()
        >>> mean_characters_per_word(x).tolist()
        [3.0, 4.0, 5.0]
    """
    name = "mean_characters_per_word"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})
    default_value = 0

    def get_function(self):
        def mean_characters_per_word(x):
            x = x.reset_index(drop=True).fillna('')
            # replace end-of-sentence punctuation with space
            p = re.escape('!,.:;?')
            end_of_sentence_punct = re.compile('[%s]+$|[%s]+ |[%s]+\n' % (p, p, p))
            x = x.str.replace(end_of_sentence_punct, ' ')
            # build DF of split words, and calculate avg length
            df = x.str.split(expand=True)
            df = df.reset_index()
            df = df.melt(id_vars='index', var_name='word_index', value_name='word')
            df['n_characters'] = df['word'].str.len()
            results = df.groupby(by=['index']).mean(numeric_only=False)['n_characters']
            return results
        return mean_characters_per_word
