# -*- coding: utf-8 -*-
import numpy as np
from featuretools.primitives.base import TransformPrimitive
from featuretools.variable_types import Numeric, Text


class UpperCaseCount(TransformPrimitive):
    """Calculates the number of upper case letters in text.

    Description:
        Given a list of strings, determine the number of characters in each string
        that are capitalized. Counts every letter individually, not just every
        word that contains capitalized letters.

        If a string is missing, return `NaN`

    Examples:
        >>> x = ['This IS a string.', 'This is a string', 'aaa']
        >>> upper_case_count = UpperCaseCount()
        >>> upper_case_count(x).tolist()
        [3.0, 1.0, 0.0]
    """
    name = "upper_case_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0

    def get_function(self):
        pattern = r'([A-Z])'

        def upper_case_count(x):
            x = x.reset_index(drop=True)
            counts = x.str.extractall(pattern).groupby(level=0).count()[0]
            counts = counts.reindex_like(x).fillna(0)
            counts[x.isnull()] = np.nan
            return counts.astype(float)
        return upper_case_count
