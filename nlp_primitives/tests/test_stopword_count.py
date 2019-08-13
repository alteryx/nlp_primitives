import featuretools as ft
import numpy as np
import pandas as pd

from ..stopword_count import StopwordCount
from ..utils import PrimitiveT, find_applicable_primitives, valid_dfs

data_path = 'nlp_primitives/data'
ft.config.set({
    'primitive_data_folder': data_path
})


class TestStopwordCount(PrimitiveT):
    primitive = StopwordCount

    def test_strings(self):
        x = pd.Series(['This is a test string.',
                       'This is second string',
                       'third string',
                       'This IS the fourth string.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([2, 1, 0, 1])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'This is a test file.'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0, 2])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
