# flake8: noqa
from nlp_primitives.version import __version__  # isort:skip

import inspect
from importlib.util import find_spec

import nltk.data
import pkg_resources
from featuretools.primitives import AggregationPrimitive, TransformPrimitive

from nlp_primitives.diversity_score import DiversityScore
from nlp_primitives.lsa import LSA
from nlp_primitives.mean_characters_per_sentence import MeanCharactersPerSentence
from nlp_primitives.number_of_sentences import NumberOfSentences
from nlp_primitives.part_of_speech_count import PartOfSpeechCount
from nlp_primitives.polarity_score import PolarityScore
from nlp_primitives.stopword_count import StopwordCount

if find_spec("tensorflow") and find_spec("tensorflow_hub"):
    from nlp_primitives.tensorflow import Elmo, UniversalSentenceEncoder

NLP_PRIMITIVES = [
    obj
    for obj in globals().values()
    if (
        inspect.isclass(obj)
        and obj is not AggregationPrimitive
        and obj is not TransformPrimitive
        and issubclass(obj, (AggregationPrimitive, TransformPrimitive))
    )
]

nltk_data_path = pkg_resources.resource_filename("nlp_primitives", "data/nltk-data/")
nltk.data.path.insert(0, nltk_data_path)
