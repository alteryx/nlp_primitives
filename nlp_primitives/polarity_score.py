import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from .utilities import clean_tokens


class PolarityScore(TransformPrimitive):
    """Calculates the polarity of a text on a scale from -1 (negative) to 1 (positive)

    Description:
        Given a list of strings assign a polarity score from -1 (negative text),
        to 0 (neutral text), to 1 (positive text). The functions returns a score
        for every given piece of text. If a string is missing, return 'NaN'

    Examples:
        >>> x = ['He loves dogs', 'She hates cats', 'There is a dog', '']
        >>> polarity_score = PolarityScore()
        >>> polarity_score(x).tolist()
        [0.677, -0.649, 0.0, 0.0]
    """
    name = "polarity_score"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})
    default_value = 0

    def get_function(self):
        dtk = TreebankWordDetokenizer()

        def polarity_score(x):
            vader = SentimentIntensityAnalyzer()
            li = []

            def vader_pol(sentence):
                return (vader.polarity_scores(sentence)['pos'] -
                        vader.polarity_scores(sentence)['neg'])
            for el in x:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    el = clean_tokens(el)
                    if len(el) < 1:
                        li.append(0.0)
                    else:
                        li.append(vader_pol(dtk.detokenize(el)))
            return pd.Series(li)
        return polarity_score
