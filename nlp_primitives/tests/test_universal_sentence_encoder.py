import sys

import featuretools as ft
import pandas as pd
import pytest
from featuretools.primitives.utils import (
    PrimitivesDeserializer,
    serialize_primitive
)

from nlp_primitives import UniversalSentenceEncoder


def test_regular(universal_sentence_encoder):
    sentences = pd.Series([
        "",
        "I like to eat pizza",
        "The roller coaster was built in 1885.",
        "When will humans go to mars?",
        "Mitochondria is the powerhouse of the cell",
    ])
    a = pd.DataFrame(universal_sentence_encoder(sentences))
    a = a.mean().round(7).astype('str')
    b = pd.Series(['-0.0007475', '0.0032088', '0.0018552', '0.0008256', '0.0028342'])
    assert a.equals(b)


@pytest.fixture()
def mock_remove_tensorflow():
    # Simulate tensorflow being missing
    tf_mod = sys.modules['tensorflow']
    sys.modules['tensorflow'] = None
    yield
    sys.modules['tensorflow'] = tf_mod


def test_without_tensorflow(universal_sentence_encoder, mock_remove_tensorflow):
    err_message = "In order to use the UniversalSentenceEncoder primitive install 'nlp_primitives[complete]'"
    with pytest.raises(ImportError) as error:
        UniversalSentenceEncoder()
    assert error.value.args[0] == err_message


def test_primitive_serialization(universal_sentence_encoder):
    sentences = pd.Series([
        "",
        "I like to eat pizza",
        "The roller coaster was built in 1885.",
        "When will humans go to mars?",
        "Mitochondria is the powerhouse of the cell",
    ])
    serialized_primitive = serialize_primitive(universal_sentence_encoder)
    deserializer = PrimitivesDeserializer()
    deserialized_primitive = deserializer.deserialize_primitive(serialized_primitive)

    a = pd.DataFrame(deserialized_primitive(sentences))
    a = a.mean().round(7).astype('str')
    b = pd.Series(['-0.0007475', '0.0032088', '0.0018552', '0.0008256', '0.0028342'])
    assert a.equals(b)


def test_feature_serialization(universal_sentence_encoder, tmpdir):
    sentences = pd.Series([
        "",
        "I like to eat pizza",
        "The roller coaster was built in 1885.",
        "When will humans go to mars?",
        "Mitochondria is the powerhouse of the cell",
    ])

    es = ft.EntitySet("es")
    df = pd.DataFrame({"id": [0, 1, 2, 3, 4], "sentences": sentences})
    es.entity_from_dataframe(dataframe=df,
                             entity_id="entity",
                             index="id",
                             variable_types={"sentences": ft.variable_types.Text})
    fm, features = ft.dfs(entityset=es,
                          target_entity="entity",
                          trans_primitives=[universal_sentence_encoder])

    filename = str(tmpdir.join("features.txt"))
    ft.save_features(features, filename)
    loaded_features = ft.load_features(filename)
    fm_serialized = ft.calculate_feature_matrix(loaded_features, entityset=es)

    pd.testing.assert_frame_equal(fm, fm_serialized)
