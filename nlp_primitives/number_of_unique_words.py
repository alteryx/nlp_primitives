import string

import nltk
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage


class NumberOfUniqueWords(TransformPrimitive):
    """Determines the number of unique words in a string.

    Description:
        Determines the number of unique words in a given string. Includes options for
        case-insensitive behavior.

    Args:
        case_insensitive (bool): Specify case_insensitivity when searching for unique words.
        For example, setting this to True would mean "WORD word" would be treated as having
        one unique word.

    Examples:
        >>> x = ['Word word Word', 'bacon, cheesburger, AND, fries', 'green red green']
        >>> number_of_unique_words = NumberOfUniqueWords()
        >>> number_of_unique_words(x).tolist()
        [2, 4, 2]

        >>> x = ['word WoRD WORD worD', 'dog dog dog', 'catt CAT caT']
        >>> number_of_unique_words = NumberOfUniqueWords(case_insensitive=True)
        >>> number_of_unique_words(x).tolist()
        [1, 1, 2]
    """

    name = "number_of_unique_words"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={"numeric"})

    default_value = 0

    def __init__(self, case_insensitive=False):
        self.case_insensitive = case_insensitive

    def get_function(self):
        def num_unique_words(array):
            unique_word_cts = []
            for text in array:
                if pd.isnull(text):
                    unique_word_cts.append(pd.NA)
                else:
                    words = nltk.tokenize.word_tokenize(text)
                    unique_words = set()
                    for word in words:
                        if self.case_insensitive:
                            word = word.lower().strip(string.punctuation)
                        else:
                            word = word.strip(string.punctuation)
                        if len(word) > 0: 
                            unique_words.add(word)
                    unique_word_cts.append(len(unique_words))
            return pd.Series(unique_word_cts)

        return num_unique_words
