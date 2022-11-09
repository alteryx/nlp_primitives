import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from nlp_primitives.utilities import clean_tokens


class PartOfSpeechCount(TransformPrimitive):
    """Calculates the occurences of each different part of speech.

    Description:
        Given a list of strings, tags each word in the string with its part of speech. 
        This method calculates the total count for each of the 15 different categories of speech.
        
        Given a list of N strings, this method will return a 15xN matrix. Each row will correspond
        to the appropriate part of speech. 
        

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['He was eating cheese', '']
        >>> part_of_speech_count = PartOfSpeechCount()
        >>> part_of_speech_count(x).tolist()
        [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0]]
    """

    name = "part_of_speech_count"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    default_value = 0

    def __init__(self):
        self.number_output_features = 15
        self.n = 15

    def get_function(self):
        types = [
            "C",
            "D",
            "E",
            "F",
            "I",
            "J",
            "L",
            "M",
            "N",
            "P",
            "R",
            "T",
            "U",
            "V",
            "W",
        ]

        def part_of_speech_count(series):
            result = []
            for element in series:
                if pd.isnull(element):
                    result.append([np.nan] * 15)
                else:
                    tags = nltk.pos_tag(clean_tokens(element))
                    fd = nltk.FreqDist(b[0] for (a, b) in tags)
                    result.append([float(fd[i]) for _ in types])
            result = (np.array(result).T).tolist()
            return pd.Series(result)

        return part_of_speech_count
