import pandas as pd

from ..universal_sentence_encoder import UniversalSentenceEncoder
from ..utils import PrimitiveT


class TestUniversalSentenceEncoder(PrimitiveT):
    primitive = UniversalSentenceEncoder

    def test_regular(self):
        primitive = self.primitive().get_function()
        sentences = pd.Series([
            "",
            "I like to eat pizza",
            "The roller coaster was built in 1885.",
            "When will humans go to mars?",
            "Mitochondria is the powerhouse of the cell",
        ])
        primitive(sentences)
