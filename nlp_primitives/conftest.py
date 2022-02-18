import pytest
import sys

from nlp_primitives.universal_sentence_encoder import UniversalSentenceEncoder


@pytest.fixture(scope="session")
def universal_sentence_encoder():
    if 'tensorflow' in sys.modules:
        return UniversalSentenceEncoder()

@pytest.fixture(autouse=True)
def add_primitives(doctest_namespace, universal_sentence_encoder):
    doctest_namespace['universal_sentence_encoder'] = universal_sentence_encoder
    

def pytest_ignore_collect(path): 
    skip_files = [
        "universal_sentence_encoder.py",
        "elmo.py"
    ]

    if 'tensorflow' not in sys.modules:
        return any([x in str(path) for x in skip_files])
   
    return False