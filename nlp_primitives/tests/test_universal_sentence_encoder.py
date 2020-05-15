import pandas as pd


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
