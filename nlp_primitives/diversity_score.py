import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from .utilities import clean_tokens


class DiversityScore(TransformPrimitive):
    """Calculates the overall complexity of the text based on the total
       number of words used in the text

    Description:
        Given a list of strings, calculates the total number of unique words
        divided by the total number of words in order to give the text a score
        from 0-1 that indicates how unique the words used in it are. This
        primitive only evaluates the 'clean' versions of strings, so ignoring cases,
        punctuation, and stopwords in its evaluation.

        If a string is missing, return `NaN`

    Examples:
        >>> diversity_score = DiversityScore()
        >>> diversity_score(["hi hi hi", "hello its me", "hey what hey what", "a dog ate a basket"]).tolist()
        [0.3333333333333333, 1.0, 0.5, 1.0]
    """
    name = "diversity_score"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})
    default_value = 0

    def get_function(self):

        def diversity_score(x):
            li = []
            for el in x:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    el = clean_tokens(el)
                    if len(el) < 1:
                        li.append(0.0)
                    else:
                        li.append(float(len(set(el))) / float(len(el)))
            return pd.Series(li)
        return diversity_score
