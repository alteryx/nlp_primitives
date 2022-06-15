# flake8: noqa
from .version import __version__  # isort:skip

from importlib.util import find_spec

import nltk.data
import pkg_resources

from .count_string import CountString
from .diversity_score import DiversityScore
from .lsa import LSA
from .mean_characters_per_word import MeanCharactersPerWord
from .median_word_length import MedianWordLength
from .num_unique_separators import NumUniqueSeparators
from .number_of_common_words import NumberOfCommonWords
from .part_of_speech_count import PartOfSpeechCount
from .polarity_score import PolarityScore
from .punctuation_count import PunctuationCount
from .stopword_count import StopwordCount
from .title_word_count import TitleWordCount
from .total_word_length import TotalWordLength
from .upper_case_count import UpperCaseCount
from .whitespace_count import WhitespaceCount

if find_spec("tensorflow") and find_spec("tensorflow_hub"):
    from .tensorflow import Elmo, UniversalSentenceEncoder


nltk_data_path = pkg_resources.resource_filename("nlp_primitives", "data/nltk-data/")
nltk.data.path.insert(0, nltk_data_path)
