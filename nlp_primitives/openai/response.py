from dataclasses import dataclass
from typing import List


class OpenAIResponse(object):
    """A response from the OpenAI API."""


@dataclass
class OpenAIEmbeddingResponse(OpenAIResponse):
    """A response from the OpenAI Embeddings API."""

    embeddings: List[List[float]]
