import numpy as np
import pandas as pd

from ..number_of_mentions import NumberOfMentions
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestNumberOfMentions(PrimitiveT):
    primitive = NumberOfMentions

    def test_regular_input(self):
        x = pd.Series(
            [
                "@hello@hi@hello",
                "@@@@andandandandand@@@",
                "andorandorand",
            ]
        )
        expected = [3.0, 1.0, 0.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_multiline(self):
        x = pd.Series(
            [
                "@\n\t\n",
                "@mention\n1@hashtag2\n@\n\n",
            ]
        )

        expected = [0.0, 2.0]
        actual = self.primitive().get_function()(x)
        np.testing.assert_array_equal(actual, expected)

    def test_null(self):
        x = pd.Series([np.nan, pd.NA, None, "@test"])

        actual = self.primitive().get_function()(x)
        expected = [np.nan, np.nan, np.nan, 1.0]
        np.testing.assert_array_equal(actual, expected)

    def test_alphanumeric_and_special(self):
        x = pd.Series(["@1or0", "@12", "#??!>@?@#>"])

        actual = self.primitive().get_function()(x)
        expected = [1.0, 1.0, 0.0]
        np.testing.assert_array_equal(actual, expected)

    def test_underscore(self):
        x = pd.Series(["@user1", "@__yes", "#??!>@?@#>"])

        actual = self.primitive().get_function()(x)
        expected = [1.0, 1.0, 0.0]
        np.testing.assert_array_equal(actual, expected)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
