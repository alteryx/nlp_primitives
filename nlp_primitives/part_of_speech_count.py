import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text

from .utilities import clean_tokens


class PartOfSpeechCount(TransformPrimitive):
    """Calculates the occurences of each different part of speech.

    Description:
        Given a list of strings, categorize each word in the string as
        a different part of speech, and return the total count for each
        of 15 different categories of speech.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['He was eating cheese', '']
        >>> part_of_speech_count = PartOfSpeechCount()
        >>> part_of_speech_count(x).tolist()
        [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0]]
    """
    name = "part_of_speech_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0

    def __init__(self):
        self.number_output_features = 15
        self.n = 15

    def get_function(self):
        types = ['C', 'D', 'E', 'F', 'I', 'J',
                 'L', 'M', 'N', 'P', 'R', 'T',
                 'U', 'V', 'W']

        def part_of_speech_count(x):
            try:
                nltk.pos_tag(" ")
            except LookupError:
                nltk.download('punkt')
                nltk.download('averaged_perceptron_tagger')
            finally:
                li = []
                for el in x:
                    if pd.isnull(el):
                        li.append([np.nan] * 15)
                    else:
                        tags = nltk.pos_tag(clean_tokens(el))
                        fd = nltk.FreqDist([b[0] for (a, b) in tags])
                        li.append([float(fd[i]) for i in types])
                li = (np.array(li).T).tolist()
                return pd.Series(li)

        return part_of_speech_count
