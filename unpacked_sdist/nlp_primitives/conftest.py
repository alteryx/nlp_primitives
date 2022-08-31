import pytest

from nlp_primitives.tensorflow.universal_sentence_encoder import (
    UniversalSentenceEncoder,
)


@pytest.fixture(scope="session")
def universal_sentence_encoder():
    return UniversalSentenceEncoder()


def pytest_addoption(parser):
    parser.addoption(
        "--notensorflow",
        action="store_true",
        default=False,
        help="If true, tests will assume tensorflow is not installed",
    )


def pytest_ignore_collect(path, config):
    skip_files = ["universal_sentence_encoder.py", "elmo.py"]

    if config.getoption("--notensorflow"):
        return any([x in str(path) for x in skip_files])

    return False
