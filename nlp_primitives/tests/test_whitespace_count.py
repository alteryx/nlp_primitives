import numpy as np
import pandas as pd

from ..whitespace_count import WhitespaceCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestWhitespaceCount(PrimitiveT):
    primitive = WhitespaceCount

    def test_strings(self):
        x = pd.Series(['', 'hi im ethan!', 'consecutive.    spaces.', ' spaces-on-ends '])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([0, 2, 4, 2])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0, 3])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
