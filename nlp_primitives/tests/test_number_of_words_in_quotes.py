import numpy as np
import pandas as pd

from ..number_of_words_in_quotes import NumberOfWordsInQuotes
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestNumberOfWordsInQuotes(PrimitiveT):
    primitive = NumberOfWordsInQuotes

    def test_regular_double_quotes_input(self):
        x = pd.Series(
            [
                'Yes "    "',
                '"Hello this is a test"',
                '"Yep, I agree"',
                '"Yep, I agree" was said amiably "well I donnot"',
            ]
        )
        expected = [0.0, 5.0, 3.0, 6.0]
        actual = self.primitive("double").get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_captures_regular_single_quotes(self):
        x = pd.Series(
            [
                "'Hello this is a test'",
                "'Yep, I agree'",
                "'Yep, I agree' was said amiably 'no i dont'",
            ]
        )
        expected = [5.0, 3.0, 6.0]
        actual = self.primitive("single").get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_captures_both_single_and_double_quotes(self):
        x = pd.Series(
            [
                "'Hello this is a test' and was replied to \"I understand!\"",
            ]
        )
        expected = [7.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_captures_contractions(self):
        x = pd.Series(["can't don't there's where's"])
        expected = [0]
        actual = self.primitive("double").get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_unicode_input(self):
        x = pd.Series(
            [
                '"Ángel"',
                '"Ángel" word word',
            ]
        )
        expected = [1.0, 1.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_multiline(self):
        x = pd.Series(
            [
                "'Yes\n, this is me'",
            ]
        )
        expected = [4.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_null(self):
        x = pd.Series([np.nan, pd.NA, None, '"test"'])

        actual = self.primitive().get_function()(x)
        expected = [np.nan, np.nan, np.nan, 1.0]
        np.testing.assert_array_equal(actual, expected)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
