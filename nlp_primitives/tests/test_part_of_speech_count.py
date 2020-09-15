import numpy as np
import pandas as pd

from ..part_of_speech_count import PartOfSpeechCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestPartOfSpeechCount(PrimitiveT):
    primitive = PartOfSpeechCount

    def test_strings(self):
        x = pd.Series(['This IS a STRING.',
                       'Testing AAA',
                       'Testing AAA-BBB',
                       'Testing AA3'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series(
            [[0., 0., 0., 1.],
             [1., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 1., 1., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [0., 0., 0., 0.],
             [2., 1., 1., 1.],
             [0., 0., 0., 0.]])

        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series(
            [[np.nan, 0.0, 0.0],
             [np.nan, 0.0, 1.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 0.0],
             [np.nan, 0.0, 2.0],
             [np.nan, 0.0, 0.0]])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)
