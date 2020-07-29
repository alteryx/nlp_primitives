import pytest

import numpy as np
import pandas as pd

from ..lsa import LSA
from ..utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestLSA(PrimitiveT):
    primitive = LSA

    def test_strings(self):
        x = pd.Series(['The dogs ate food.',
                       'She ate a pineapple',
                       'Consume Electrolytes, he told me.',
                       'Hello'])
        primitive_func = self.primitive().get_function()

        answers = np.array([[0.7751553, 0.7751553, 0., 0.], [0., 0., 1., 0.]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '#;.<',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()

        answers = np.array(
            [[np.nan, 0, 1],
             [np.nan, 0, 0]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results)

    def test_one_string(self):
        primitive_func = self.primitive().get_function()

        x = pd.Series([np.nan])
        with pytest.raises(ValueError, match='empty vocabulary'):
            primitive_func(x)

        x = pd.Series(['just one string in this example',])
        answers = np.array(
            [[1.],
             [0.]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)
