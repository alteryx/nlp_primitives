import numpy as np
import pandas as pd
import pytest

from ..mean_sentence_length import MeanSentenceLength
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestMeanSentenceLength(PrimitiveT):
    primitive = MeanSentenceLength

    def test_sentences(self):
        x = pd.Series(
            [
                "Ab. Bb. Db.",
                "And? Why! Box. Car? Rat.",
                "Yep.",
            ]
        )
        primitive_func = self.primitive().get_function()
        answers = pd.Series([3.0, 4.0, 4.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_multiline(self):
        x = pd.Series(
            [
                "This is.",
                "This is. This is. Not. Not.",
                "and more",
            ]
        )
        primitive_func = self.primitive().get_function()
        answers = pd.Series([8.0, 6.0, 8.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    @pytest.mark.parametrize(
        "na_value",
        [None, np.nan, pd.NA],
    )
    def test_nans(self, na_value):
        x = pd.Series([na_value, "", "third line"])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, 0, 10.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    @pytest.mark.parametrize(
        "na_value",
        [None, np.nan, pd.NA],
    )
    def test_all_nans(self, na_value):
        x = pd.Series([na_value, na_value, na_value])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, np.nan, np.nan])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())