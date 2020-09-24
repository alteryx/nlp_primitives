import numpy as np
import pandas as pd

from ..upper_case_count import UpperCaseCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestUpperCaseCount(PrimitiveT):
    primitive = UpperCaseCount

    def test_strings(self):
        x = pd.Series(['This IS a STRING.',
                       'Testing AaA',
                       'Testing AAA-BBB',
                       'testing aaa'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([9.0, 3.0, 7.0, 0.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0.0, 9.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
