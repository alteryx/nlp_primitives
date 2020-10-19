import pytest

from nlp_primitives.universal_sentence_encoder import UniversalSentenceEncoder


@pytest.fixture(scope="session")
def universal_sentence_encoder():
    return UniversalSentenceEncoder()


@pytest.fixture(autouse=True)
def add_primitives(doctest_namespace, universal_sentence_encoder):
    doctest_namespace['universal_sentence_encoder'] = universal_sentence_encoder
