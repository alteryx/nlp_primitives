import numpy as np
import pandas as pd

from ..polarity_score import PolarityScore
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestPolarityScore(PrimitiveT):
    primitive = PolarityScore

    def test_primitive_func_1(self):
        array = pd.Series(['He hates cars!',
                           'She loves everything',
                           'This is neutral',
                           '!12323'])
        primitive_instance = self.primitive()
        primitive_func = primitive_instance.get_function()
        answer = pd.Series([-0.649, 0.677, 0.0, 0.0])
        pd.testing.assert_series_equal(primitive_func(array), answer,
                                       check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan, '', 'Negativity!! ,,'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series([np.nan, 0.0, -1.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()

        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
