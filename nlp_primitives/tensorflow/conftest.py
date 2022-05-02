import pytest


@pytest.fixture(autouse=True)
def add_primitives(doctest_namespace, universal_sentence_encoder):
    doctest_namespace["universal_sentence_encoder"] = universal_sentence_encoder
