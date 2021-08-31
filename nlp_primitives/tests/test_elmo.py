import numpy as np
import pandas as pd

from ..elmo import Elmo
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestElmo(PrimitiveT):
    primitive = Elmo

    def test_regular(self):
        primitive = self.primitive().get_function()
        words = pd.Series([
            "",
            "I like to eat pizza",
            "The roller coaster was built in 1885.",
            "When will humans go to mars?",
            "Mitochondria is the powerhouse of the cell",
        ])
        new_results = primitive(words)
        assert round(sum(new_results[:, 0]), 3) == 8.744
        assert round(sum(new_results[:, 1]), 3) == 2.774
        assert round(sum(new_results[:, 2]), 3) == -8.852
        assert round(sum(new_results[:, 3]), 3) == -2.433
        assert round(sum(new_results[:, 4]), 3) == -13.623
        answer0 = new_results[:5, 0].round(5)
        answer1 = new_results[:5, 1].round(5)
        answer2 = new_results[:5, 2].round(5)
        answer3 = new_results[:5, 3].round(5)
        answer4 = new_results[:5, 4].round(5)
        correct0 = np.array([-0.19886, -0.30473, 0.28911, -0.1545, -0.08023]).round(5)
        correct1 = np.array([-0.3457, -0.45462, 0.25379, 0.02318, 0.33729]).round(5)
        correct2 = np.array([-0.07041, -0.09047, -0.26982, 0.03027, -0.5508]).round(5)
        correct3 = np.array([0.25077, -0.01977, -0.10443, -0.26923, 0.453]).round(5)
        correct4 = np.array([-0.21744, 0.71178, -0.04611, -0.02631, -0.44973]).round(5)
        np.testing.assert_allclose(correct0, answer0, rtol=1e-04)
        np.testing.assert_allclose(correct1, answer1, rtol=1e-04)
        np.testing.assert_allclose(correct2, answer2, rtol=1e-04)
        np.testing.assert_allclose(correct3, answer3, rtol=1e-04)
        np.testing.assert_allclose(correct4, answer4, rtol=1e-04)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(),
                  multi_output=True, max_features=100, instance_ids=[0])
