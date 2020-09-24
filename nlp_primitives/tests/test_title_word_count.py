import numpy as np
import pandas as pd

from ..title_word_count import TitleWordCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestTitleWordCount(PrimitiveT):
    primitive = TitleWordCount

    def test_strings(self):
        x = pd.Series(['My favorite movie is Jaws.',
                       'this is a string',
                       'AAA',
                       'I bought a Yo-Yo'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([2.0, 0.0, 1.0, 2.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'My favorite movie is Jaws.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0.0, 2.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
