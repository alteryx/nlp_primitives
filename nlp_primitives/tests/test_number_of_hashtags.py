import numpy as np
import pandas as pd

from ..number_of_hashtags import NumberOfHashtags
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestNumberOfHashtags(PrimitiveT):
    primitive = NumberOfHashtags

    def test_regular_input(self):
        x = pd.Series(
            [
                "#hello#hi#hello",
                "#############and",
                "andorandorandorandor",
            ]
        )
        expected = pd.Series([3.0, 1.0, 0.0])
        actual = self.primitive().get_function()(x)
        pd.testing.assert_series_equal(actual, expected, check_names=False)

    def test_multiline(self):
        x = pd.Series(
            [
                "#\n\t\n",
                "#hashtag\n1#hashtag2\n#\n\n",
            ]
        )

        expected = pd.Series([0.0, 2.0])
        actual = self.primitive().get_function()(x)
        pd.testing.assert_series_equal(actual, expected, check_names=False)

    def test_null(self):
        x = pd.Series([np.nan, pd.NA, None, "#test"])

        actual = self.primitive().get_function()(x)
        expected = pd.Series([np.nan, np.nan, np.nan, 1.0])
        pd.testing.assert_series_equal(actual, expected, check_names=False)

    def test_alphanumeric_and_special(self):
        x = pd.Series(["#1or0", "#12", "#??!>@?@#>"])

        actual = self.primitive().get_function()(x)
        expected = pd.Series([1.0, 1.0, 0.0])
        pd.testing.assert_series_equal(actual, expected, check_names=False)

    def test_underscore(self):
        x = pd.Series(["#no", "#__yes", "#??!>@?@#>"])

        actual = self.primitive().get_function()(x)
        expected = pd.Series([1.0, 1.0, 0.0])
        pd.testing.assert_series_equal(actual, expected, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())