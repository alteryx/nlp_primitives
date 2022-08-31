import numpy as np
import pandas as pd

from nlp_primitives.number_of_sentences import NumberOfSentences
from nlp_primitives.tests.test_utils import (
    PrimitiveT,
    find_applicable_primitives,
    valid_dfs,
)


class TestNumberOfSentences(PrimitiveT):
    primitive = NumberOfSentences

    def test_regular_input(self):
        x = pd.Series(
            [
                "Hello. Hello! Hello? Hello.",
                "and?",
                "yes no",
            ]
        )
        expected = [4.0, 1.0, 1.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_unicode_input(self):
        x = pd.Series(["Ángel is here.", "Ángel is here áèí! I am not."])
        expected = [1.0, 2.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_multiline(self):
        x = pd.Series(
            [
                "Yes\n, this is true!",
            ]
        )

        expected = [1.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_null(self):
        x = pd.Series([np.nan, pd.NA, None, ""])

        actual = self.primitive().get_function()(x)
        expected = [np.nan, np.nan, np.nan, 0.0]
        np.testing.assert_array_equal(actual, expected)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
