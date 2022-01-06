import numpy as np
import pandas as pd

from ..token_count import TokenCount
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestTokenCount(PrimitiveT):
    primitive = TokenCount

    def test_token_count_arguments(self):
        x = pd.Series(['This is the first document.',
                       'This document is the second document.',
                       'And this is the third one.',
                       'Is this the first document?', ])
        expected = np.array([[0, 0, 1, 0],
                            [0, 1, 0, 0],
                            [1, 0, 0, 1],
                            [1, 1, 1, 0],
                            [0, 0, 0, 1],
                            [0, 1, 0, 0],
                            [1, 0, 0, 1],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 1, 0],
                            [0, 1, 0, 0],
                            [1, 0, 1, 0],
                            [0, 0, 0, 1]])

        test_primitive = self.primitive(analyzer='word', ngram_range=(2, 2))
        actual = test_primitive.get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_multiline(self):
        x = pd.Series(['First line!',
                       'second line\nthird line\n fourth line'])
        expected = np.array([[1., 0.],
                             [0., 1.],
                             [1., 3.],
                             [0., 1.],
                             [0., 1.]])
        test_primitive = self.primitive()
        actual = test_primitive.get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_null(self):
        x = pd.Series([np.nan,
                       pd.NA,
                       None,
                       'Hi Bob',
                       'hi sam'])

        expected = np.array([[np.nan, np.nan, np.nan, 1., 0.],
                             [np.nan, np.nan, np.nan, 1., 1.],
                             [np.nan, np.nan, np.nan, 0., 1.]])
        test_primitive = self.primitive()
        actual = test_primitive.get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)
