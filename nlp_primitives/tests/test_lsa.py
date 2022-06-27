import nltk
import numpy as np
import pandas as pd
import pytest

from ..lsa import LSA
from .test_utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestLSA(PrimitiveT):
    primitive = LSA

    def test_strings(self):
        x = pd.Series(
            [
                "The dogs ate food.",
                "She ate a pineapple",
                "Consume Electrolytes, he told me.",
                "Hello",
            ]
        )
        primitive_func = self.primitive().get_function()

        answers = pd.Series(
            [
                [
                    0.06130623793383833,
                    0.01745556451033845,
                    0.0057337659660533094,
                    0.0002763538434776728,
                ],
                [
                    -0.04393122671005984,
                    0.04819242528049181,
                    0.01643423390395579,
                    0.0011141016579207792,
                ],
            ]
        )
        results = primitive_func(x)
        np.testing.assert_array_almost_equal(
            np.concatenate(([np.array(answers[0])], [np.array(answers[1])]), axis=0),
            np.concatenate(([np.array(results[0])], [np.array(results[1])]), axis=0),
            decimal=2,
        )

    def test_strings_custom_corpus(self):
        x = pd.Series(
            [
                "The dogs ate food.",
                "She ate a pineapple",
                "Consume Electrolytes, he told me.",
                "Hello",
            ]
        )
        # Create a new corpus using only the first 10000 elements from Gutenberg
        gutenberg = nltk.corpus.gutenberg.sents()
        corpus = [" ".join(sent) for sent in gutenberg]
        corpus = corpus[:10000]
        primitive_func = self.primitive(corpus=corpus).get_function()

        answers = pd.Series(
            [
                [0.03858566832087156, 0.04979961879358504, 0.013042488281432613, 0.0],
                [
                    -0.0010495388842080527,
                    -0.0011128696986250912,
                    0.001556757056617563,
                    0.0,
                ],
            ]
        )
        results = primitive_func(x)
        np.testing.assert_array_almost_equal(
            np.concatenate(([np.array(answers[0])], [np.array(answers[1])]), axis=0),
            np.concatenate(([np.array(results[0])], [np.array(results[1])]), axis=0),
            decimal=2,
        )

    def test_nan(self):
        x = pd.Series([np.nan, "#;.<", "This IS a STRING."])
        primitive_func = self.primitive().get_function()

        answers = pd.Series([[np.nan, 0, 0.06], [np.nan, 0, 0.06]])
        results = primitive_func(x)
        np.testing.assert_array_almost_equal(
            np.concatenate(([np.array(answers[0])], [np.array(answers[1])]), axis=0),
            np.concatenate(([np.array(results[0])], [np.array(results[1])]), axis=0),
            decimal=2,
        )

    def test_seed(self):
        prim = self.primitive(random_seed=1)
        # trigger trainer creation via get_function
        _ = prim.get_function()
        # trainer.steps returns list of tuples representing pipeline steps
        # tuple has form ("component_name", component_object)
        assert prim.trainer.steps[1][1].random_state == 1

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(
            es, aggregation, transform, self.primitive.name.upper(), multi_output=True
        )

    def test_bad_algorithm_input_value(self):
        err_message = "TruncatedSVD algorithm must be either 'randomized' or 'arpack'"
        with pytest.raises(ValueError, match=err_message):
            LSA(algorithm="bad_algo")

    def test_args_strings(self):
        # With default values args string should be empty
        args_string = self.primitive().get_args_string()
        assert args_string == ""

        # Should include arpack
        args_string = self.primitive(algorithm="arpack").get_args_string()
        assert args_string == ", algorithm=arpack"

        # Should display "user_defined" instead of full custom corpus
        custom_corpus = ["I", "am", "a", "custom", "corpus"]
        args_string = self.primitive(corpus=custom_corpus).get_args_string()
        assert args_string == ", corpus=user_defined"

        # Test all args
        args_string = self.primitive(
            random_seed=100, corpus=custom_corpus, algorithm="arpack"
        ).get_args_string()
        assert args_string == ", random_seed=100, corpus=user_defined, algorithm=arpack"
