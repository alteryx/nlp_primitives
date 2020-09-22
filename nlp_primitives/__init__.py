# flake8: noqa
__version__ = '1.0.0'
from os import path
import pkg_resources
import shutil
import tempfile

from .diversity_score import DiversityScore
from .lsa import LSA
from .mean_characters_per_word import MeanCharactersPerWord
from .part_of_speech_count import PartOfSpeechCount
from .polarity_score import PolarityScore
from .punctuation_count import PunctuationCount
from .stopword_count import StopwordCount
from .title_word_count import TitleWordCount
from .universal_sentence_encoder import UniversalSentenceEncoder
from .upper_case_count import UpperCaseCount


fp = pkg_resources.resource_filename('nlp_primitives', 'data/nltk-data.tar.gz')
dp = path.normpath(path.join(fp, '../nltk-data'))
try:
    tf = tempfile.mkdtemp()
    shutil.unpack_archive(fp, tf)
    if path.exists(dp):
        shutil.rmtree(dp)
    shutil.copytree(tf, dp)
finally:
    shutil.rmtree(tf)