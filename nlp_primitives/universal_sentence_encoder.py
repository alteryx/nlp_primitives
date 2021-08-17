from featuretools.primitives import TransformPrimitive
from featuretools.utils.gen_utils import import_or_raise
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class UniversalSentenceEncoder(TransformPrimitive):
    """Transforms a sentence or short paragraph to a vector using [tfhub
    model](https://tfhub.dev/google/universal-sentence-encoder/2)

    Args:
        None

    Examples:
        >>> sentences = ["I like to eat pizza", "The roller coaster was built in 1885.", ""]
        >>> # universal_sentence_encoder = UniversalSentenceEncoder()  # normal syntax
        >>> output = universal_sentence_encoder(sentences)  # defined in test file
        >>> len(output)
        512
        >>> len(output[0])
        3
        >>> values = output[:3, 0]
        >>> [round(x, 4) for x in values]
        [0.0178, 0.0616, -0.0089]
    """
    name = "universal_sentence_encoder"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={'numeric'})

    def __init__(self):
        message = "In order to use the UniversalSentenceEncoder primitive install 'nlp_primitives[complete]'"
        self.tf = import_or_raise("tensorflow", message)
        hub = import_or_raise("tensorflow_hub", message)
        self.tf.compat.v1.disable_eager_execution()
        self.module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        self.embed = hub.Module(self.module_url)
        self.number_output_features = 512
        self.n = 512

    def get_function(self):
        def universal_sentence_encoder(col):
            with self.tf.compat.v1.Session() as session:
                session.run([self.tf.compat.v1.global_variables_initializer(),
                             self.tf.compat.v1.tables_initializer()])
                embeddings = session.run(self.embed(col.tolist()))
            return embeddings.transpose()
        return universal_sentence_encoder
