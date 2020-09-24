import numpy as np
import pandas as pd

from ..punctuation_count import PunctuationCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestPunctuationCount(PrimitiveT):
    primitive = PunctuationCount

    def test_punctuation(self):
        x = pd.Series(['This is a test file.',
                       'This, is second line?',
                       'third/line $1,000;',
                       'and--subsequen\'t lines...',
                       '*and, more..'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([1.0, 2.0, 4.0, 6.0, 4.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_multiline(self):
        x = pd.Series(['This is a test file.',
                       'This is second line\nthird line $1000;\nand subsequent lines'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([1.0, 2.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'This is a test file.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0.0, 1.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
