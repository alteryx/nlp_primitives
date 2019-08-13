import numpy as np
import pandas as pd

from ..universal_sentence_encoder import UniversalSentenceEncoder
from ..utils import PrimitiveT  # find_applicable_primitives, valid_dfs


class TestUniversalSentenceEncoder(PrimitiveT):
    primitive = UniversalSentenceEncoder

    def test_regular(self):
        primitive = self.primitive().get_function()
        sentences = pd.Series([
            "",
            "I like to eat pizza",
            "The roller coaster was built in 1885.",
            "When will humans go to mars?",
            "Mitochondria is the powerhouse of the cell",
        ])
        new_results = primitive(sentences)
        assert round(sum(new_results[:, 0]), 3) == -0.383
        assert round(sum(new_results[:, 1]), 3) == 1.643
        assert round(sum(new_results[:, 2]), 3) == 0.950
        assert round(sum(new_results[:, 3]), 3) == 0.423
        assert round(sum(new_results[:, 4]), 3) == 1.451
        answer0 = new_results[:5, 0].round(5)
        answer1 = new_results[:5, 1].round(5)
        answer2 = new_results[:5, 2].round(5)
        answer3 = new_results[:5, 3].round(5)
        answer4 = new_results[:5, 4].round(5)
        correct0 = np.array([0.005107, -0.011806, -0.048946, 0.005020, 0.019708]).round(5)
        correct1 = np.array([0.017786, 0.061581, -0.008888, 0.034359, 0.044404]).round(5)
        correct2 = np.array([-0.007204, 0.039610, -0.055290, 0.037506, 0.009574]).round(5)
        correct3 = np.array([-0.059914, 0.008037, -0.053351, 0.018910, 0.031320]).round(5)
        correct4 = np.array([-0.029039, 0.071482, 0.001880, 0.052682, -0.047268]).round(5)
        np.testing.assert_allclose(correct0, answer0, rtol=1e-04)
        np.testing.assert_allclose(correct1, answer1, rtol=1e-04)
        np.testing.assert_allclose(correct2, answer2, rtol=1e-04)
        np.testing.assert_allclose(correct3, answer3, rtol=1e-04)
        np.testing.assert_allclose(correct4, answer4, rtol=1e-04)

    # def test_with_featuretools(self, es):
    #     transform, aggregation = find_applicable_primitives(self.primitive)
    #     primitive_instance = self.primitive()
    #     transform.append(primitive_instance)
    #     valid_dfs(es, aggregation[1:2], transform[-10:], self.primitive.name.upper(), multi_output=True,
    #               target_entity='customers', max_features=30, instance_ids=[0], max_depth=2)
