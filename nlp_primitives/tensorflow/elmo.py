from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage


class Elmo(TransformPrimitive):
    """Transforms a sentence or short paragraph using deep
    contextualized langauge representations. Usese the following
    pre-trained model [tfhub model](https://tfhub.dev/google/elmo/2)

    Args:
        None

    Examples:
        >>> Elmo = Elmo()
        >>> words = ["I like to eat pizza",
        ...          "The roller coaster was built in 1885.",
        ...          "When will humans go to mars?"]
        >>> output = Elmo(words)
        >>> len(output)
        1024
        >>> len(output[0])
        3
        >>> values = output[:3, 0]
        >>> [round(x, 4) for x in values]
        [-0.3457, -0.4546, 0.2538]
    """
    name = "elmo"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags="numeric")

    def __init__(self):
        self.handle = "https://tfhub.dev/google/elmo/2"
        self.number_output_features = 1024
        self.n = 1024

    def install(self):
        import tensorflow as tf
        import tensorflow_hub as hub

        with tf.compat.v1.Session():
            tf.compat.v1.global_variables_initializer().run()
            self.embed = hub.Module(self.handle)

    def get_function(self):
        self.install()

        def elmo(col):
            import tensorflow as tf

            with tf.compat.v1.Session() as session:
                session.run([tf.compat.v1.global_variables_initializer(),
                             tf.compat.v1.tables_initializer()])
                embeddings = session.run(self.embed(col.tolist()))
            return embeddings.transpose()
        return elmo
