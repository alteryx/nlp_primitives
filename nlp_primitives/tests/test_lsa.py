import numpy as np
import pandas as pd

from ..lsa import LSA
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestLSA(PrimitiveT):
    primitive = LSA

    def test_strings(self):
        x = pd.Series(['The dogs ate food.',
                       'She ate a pineapple',
                       'Consume Electrolytes, he told me.',
                       'Hello'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series(
            [[0.06130623793383833, 0.01745556451033845, 0.0057337659660533094, 0.0002763538434776728],
             [-0.04393122671005984, 0.04819242528049181, 0.01643423390395579, 0.0011141016579207792]])
        results = primitive_func(x)
        np.testing.assert_array_almost_equal(np.concatenate(([np.array(answers[0])], [np.array(answers[1])]), axis=0),
                                             np.concatenate(([np.array(results[0])], [np.array(results[1])]), axis=0),
                                             decimal=2)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '#;.<',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()

        answers = pd.Series(
            [[np.nan, 0, 0.06],
             [np.nan, 0, 0.06]])
        results = primitive_func(x)
        np.testing.assert_array_almost_equal(np.concatenate(([np.array(answers[0])], [np.array(answers[1])]), axis=0),
                                             np.concatenate(([np.array(results[0])], [np.array(results[1])]), axis=0),
                                             decimal=2)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)
