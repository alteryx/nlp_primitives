import numpy as np
import pandas as pd

from ..diversity_score import DiversityScore
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestDiversityScore(PrimitiveT):
    primitive = DiversityScore

    def test_primitive_func_1(self):
        array = pd.Series(['This is a diverse string.',
                           'Not diverse not diverse not',
                           'this is a semi diverse diverse example',
                           'a a'])
        primitive_instance = self.primitive()
        primitive_func = primitive_instance.get_function()
        answer = pd.Series([1.0, 0.6666666666666666, 0.75, 0.0])
        pd.testing.assert_series_equal(primitive_func(array), answer,
                                       check_names=False)

    def test_nan(self):
        x = pd.Series([np.nan, '', 'This! ^is,, : o,, #punctuation.'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series([np.nan, 0.0, 1.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()

        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
