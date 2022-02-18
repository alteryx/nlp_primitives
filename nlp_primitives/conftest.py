import sys

import pytest

from nlp_primitives.universal_sentence_encoder import UniversalSentenceEncoder


@pytest.fixture(scope="session")
def universal_sentence_encoder(pytestconfig):
    if not pytestconfig.getoption("--notensorflow"):
        return UniversalSentenceEncoder()
    else:
        return None


@pytest.fixture(autouse=True)
def add_primitives(doctest_namespace, universal_sentence_encoder):
    doctest_namespace['universal_sentence_encoder'] = universal_sentence_encoder


def pytest_addoption(parser):
    parser.addoption(
        "--notensorflow",
        action="store_true",
        default=False,
        help="If true, tests will assume tensorflow is not installed",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "notensorflow: mark test to be skipped if tensorflow is not installed"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--notensorflow"):
        skip_notensorflow = pytest.mark.skip(reason="no tensorflow installed")
        for item in items:
            if "notensorflow" in item.keywords:
                item.add_marker(skip_notensorflow)


def pytest_ignore_collect(path, config):
    skip_files = [
        "universal_sentence_encoder.py",
        "elmo.py"
    ]

    if config.getoption("--notensorflow"):
        return any([x in str(path) for x in skip_files])

    return False
