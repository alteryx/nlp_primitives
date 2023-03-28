from dataclasses import dataclass
from typing import Generic, List, TypeVar

import openai
from nlp_primitives.openai.model import OpenAIEmbeddingModel
from nlp_primitives.openai.response import OpenAIEmbeddingResponse, OpenAIResponse

RESPONSE = TypeVar("RESPONSE", bound=OpenAIResponse)


class OpenAIRequest(Generic[RESPONSE]):
    """A request to the OpenAI API."""

    token_consumption: int

    async def execute(self) -> RESPONSE:
        raise NotImplementedError("Subclass must implement")


class OpenAIEmbeddingRequest(OpenAIRequest[OpenAIEmbeddingResponse]):
    """A request to the OpenAI Embeddings API."""

    def __init__(
        self,
        list_of_text: List[str],
        model: OpenAIEmbeddingModel,
        token_consumption: int,
    ):
        self.list_of_text = [text.replace("\n", " ") for text in list_of_text]
        self.model = model
        self.token_consumption = token_consumption

    async def execute(self) -> OpenAIEmbeddingResponse:
        data = (
            await openai.Embedding.acreate(
                input=self.list_of_text, engine=self.model.name
            )
        ).data
        data = sorted(
            data, key=lambda x: x["index"]
        )  # maintain the same order as input.
        return OpenAIEmbeddingResponse(embeddings=[d["embedding"] for d in data])


@dataclass
class StaticOpenAIEmbeddingRequest(OpenAIRequest[OpenAIEmbeddingResponse]):
    """A request to the OpenAI Embeddings API that immediately returns a static value.
    """

    result: List[List[float]]
    token_consumption = 0

    async def execute(self) -> OpenAIEmbeddingResponse:
        return OpenAIEmbeddingResponse(embeddings=self.result)
