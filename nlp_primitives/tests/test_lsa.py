import pytest

import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, Pipeline

from ..lsa import LSA, make_trainer
from ..utils import PrimitiveT, find_applicable_primitives, valid_dfs


class TestLSA(PrimitiveT):
    primitive = LSA

    def test_strings(self):
        x = pd.Series(['The dogs ate food.',
                       'She ate a pineapple',
                       'Consume Electrolytes, he told me.',
                       'Hello'])
        primitive_func = self.primitive().get_function()

        answers = np.array(
            [[0.06130623793383833, 0.01745556451033845, 0.0057337659660533094, 0.0002763538434776728],
             [-0.04373122671005984, 0.04859242528049181, 0.01643423390395579, 0.0011141016579207792]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results, decimal=4)

    def test_nan(self):
        x = pd.Series([np.nan,
                       '#;.<',
                       'This IS a STRING.'])
        primitive_func = self.primitive().get_function()

        answers = np.array(
            [[np.nan, 0, 0.073817],
             [np.nan, 0, -0.023258]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results, decimal=4)

    def test_one_string(self):
        primitive_func = self.primitive().get_function()

        x = pd.Series([np.nan])
        with pytest.raises(ValueError, match='Found array with 0'):
            primitive_func(x)

        x = pd.Series(['just one string in this example',])
        answers = np.array(
            [[ 0.026843],
             [-0.001465]])
        results = np.array(primitive_func(x).values.tolist())
        np.testing.assert_array_almost_equal(answers, results)

    def test_invalid_trainer(self):
        with pytest.raises(ValueError, match='not a Pipeline object'):
            LSA(trainer=TruncatedSVD())
        with pytest.raises(ValueError, match='incorrect number of transformers'):
            LSA(trainer=make_pipeline(TruncatedSVD()))
        with pytest.raises(ValueError, match='have a TfIdfVectorizer as its first transformer'):
            LSA(trainer=make_pipeline(TruncatedSVD(), TruncatedSVD()))
        with pytest.raises(ValueError, match='have a TruncatedSVD as its second transformer'):
            LSA(trainer=make_pipeline(TfidfVectorizer(), TfidfVectorizer()))
        with pytest.raises(ValueError, match='should be pre-fitted'):
            LSA(trainer=make_pipeline(TfidfVectorizer(), TruncatedSVD()))

    def test_valid_trainer(self, es):
        corpus = ['this is a very small corpus', 'that will be able to be trained nonetheless']
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = LSA(trainer=make_trainer(corpus))
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper(), multi_output=True)
