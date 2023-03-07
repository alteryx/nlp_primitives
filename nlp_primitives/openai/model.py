from dataclasses import dataclass


@dataclass
class OpenAIModel(object):
    """A model accessible via the OpenAI API."""

    name: str
    encoding: str
    max_tokens: int


@dataclass
class OpenAIEmbeddingModel(OpenAIModel):
    """A model accessible via the OpenAI API that can produce embeddings."""

    output_dimensions: int
