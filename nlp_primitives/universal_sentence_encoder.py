import tensorflow as tf
import tensorflow_hub as hub
from featuretools.primitives import TransformPrimitive
from featuretools.variable_types import Numeric, Text


class UniversalSentenceEncoder(TransformPrimitive):
    """Transforms a sentence or short paragraph to a vector using [tfhub
    model](https://tfhub.dev/google/universal-sentence-encoder/2)

    Args:
        None

    Examples:
        >>> sentences = ["I like to eat pizza", "The roller coaster was built in 1885.", ""]
        >>> output = universal_sentence_encoder(sentences)
        >>> len(output)
        512
        >>> len(output[0])
        3
        >>> values = output[:3, 0]
        >>> [round(x, 4) for x in values]
        [0.0178, 0.0616, -0.0089]
    """
    name = "universal_sentence_encoder"
    input_types = [Text]
    return_type = Numeric

    def __init__(self):
        tf.compat.v1.disable_eager_execution()
        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        self.embed = hub.Module(self.module_url)
        self.number_output_features = 512
        self.n = 512

    def get_function(self):
        def universal_sentence_encoder(col):
            with tf.compat.v1.Session() as session:
                session.run([tf.compat.v1.global_variables_initializer(),
                             tf.compat.v1.tables_initializer()])
                embeddings = session.run(self.embed(col.tolist()))
            return embeddings.transpose()
        return universal_sentence_encoder
