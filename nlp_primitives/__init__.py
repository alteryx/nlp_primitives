# flake8: noqa
from nlp_primitives.version import __version__  # isort:skip

from importlib.util import find_spec

import nltk.data
import pkg_resources

from nlp_primitives.count_string import CountString
from nlp_primitives.diversity_score import DiversityScore
from nlp_primitives.lsa import LSA
from nlp_primitives.mean_characters_per_word import MeanCharactersPerWord
from nlp_primitives.median_word_length import MedianWordLength
from nlp_primitives.num_unique_separators import NumUniqueSeparators
from nlp_primitives.number_of_common_words import NumberOfCommonWords
from nlp_primitives.part_of_speech_count import PartOfSpeechCount
from nlp_primitives.polarity_score import PolarityScore
from nlp_primitives.punctuation_count import PunctuationCount
from nlp_primitives.stopword_count import StopwordCount
from nlp_primitives.title_word_count import TitleWordCount
from nlp_primitives.total_word_length import TotalWordLength
from nlp_primitives.upper_case_count import UpperCaseCount
from nlp_primitives.whitespace_count import WhitespaceCount

if find_spec("tensorflow") and find_spec("tensorflow_hub"):
    from nlp_primitives.tensorflow import Elmo, UniversalSentenceEncoder


nltk_data_path = pkg_resources.resource_filename("nlp_primitives", "data/nltk-data/")
nltk.data.path.insert(0, nltk_data_path)
