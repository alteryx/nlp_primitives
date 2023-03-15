import asyncio
import itertools
from typing import List, Optional

import nest_asyncio
import numpy as np
import pandas as pd
import tiktoken
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, NaturalLanguage

from nlp_primitives.openai.api_requester import process_api_requests
from nlp_primitives.openai.model import (
    OpenAIEmbeddingModel,
)
from nlp_primitives.openai.request import (
    OpenAIEmbeddingRequest,
    OpenAIRequest,
    StaticOpenAIEmbeddingRequest,
)
from nlp_primitives.openai.response import OpenAIEmbeddingResponse

DEFAULT_MODEL = OpenAIEmbeddingModel(
    name="text-embedding-ada-002",
    encoding="cl100k_base",
    max_tokens=8191,
    output_dimensions=1536,
)


class OpenAIEmbeddings(TransformPrimitive):
    """Generates embeddings using OpenAI.

    Description:
        Given list of strings, determine the embeddings for each string, using
        the OpenAI model.

    Args:
        model (OpenAIEmbeddingModel, optional): The model to use to produce embeddings.
            Defaults to "text-embedding-ada-002" if not specified.
        max_tokens_per_batch (int, optional): The maximum number of tokens to send in a batched request to OpenAI.
            Defaults to 10 * model.max_tokens if not specified.

    Examples:
        >>> x = ['This is a test file', 'This is second line', None]
        >>> openai_embeddings = OpenAIEmbeddings()
        >>> openai_embeddings(x).tolist()
        [
          [
            -0.007940744049847126,
            0.007481361739337444,
            ...
            0.009351702407002449,
            -0.016065239906311035
          ],
          [
            -0.001055666827596724,
            0.01066350657492876,
            ...
            -0.024650879204273224,
            0.009666346944868565
          ],
          [
            nan,
            nan,
            ...
            nan,
            nan
          ],
        ]
    """

    name = "openai_embeddings"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})

    def __init__(
        self,
        model: OpenAIEmbeddingModel = DEFAULT_MODEL,
        max_tokens_per_batch: Optional[int] = None,
    ):
        self.model = model
        self.number_output_features = model.output_dimensions
        if max_tokens_per_batch is None:
            self.max_tokens_per_batch = model.max_tokens * 10
        else:
            self.max_tokens_per_batch = max_tokens_per_batch

    def _is_too_many_tokens(self, element, encoding) -> bool:
        """Return whether a data element has too many tokens and should be ignored"""
        return len(encoding.encode(element)) > self.model.max_tokens

    def _create_request_batches(
        self, series
    ) -> List[OpenAIRequest[OpenAIEmbeddingResponse]]:
        """Group elements of a series into batches of requests to send to OpenAI"""
        # the encoding used by the model
        encoding = tiktoken.get_encoding(self.model.encoding)

        # a static embeddings response for an invalid element
        invalid_request = StaticOpenAIEmbeddingRequest(
            result=[np.nan] * self.number_output_features
        )

        # mutable variables to track the request batching process
        # a running list of the requests to make
        requests: List[OpenAIRequest[OpenAIEmbeddingResponse]] = []
        # a list of elements that should be batched into the next request
        elements_in_batch = []
        # a running total of tokens that will be sent in the next request
        tokens_in_batch = 0

        def add_batched_request() -> int:
            """Create a batched request from the currently staged elements and add it to the request list. Return the resulting total of tokens that will be sent in the next request. 
            """
            if elements_in_batch:
                requests.append(
                    OpenAIEmbeddingRequest(
                        list_of_text=elements_in_batch.copy(),
                        model=self.model,
                        token_consumption=tokens_in_batch,
                    )
                )
                elements_in_batch.clear()
                return 0
            else:
                return tokens_in_batch

        def can_fit_in_batch(tokens) -> bool:
            return (
                len(elements_in_batch) < 2048
                and tokens_in_batch + tokens <= self.max_tokens_per_batch
            )

        # loop through the input data series to create request batches
        for element in series:
            if pd.isnull(element) or self._is_too_many_tokens(element, encoding):
                # invalid element
                # create a request from any pending elements
                tokens_in_batch = add_batched_request()
                # add a static request that returns the invalid results
                requests.append(invalid_request)
            else:
                # valid element
                # check how many tokens are in it
                next_tokens = len(encoding.encode(element))

                # can this element fit in the batch?
                if can_fit_in_batch(next_tokens):
                    # can't fit -- construct a request with existing elements
                    tokens_in_batch = add_batched_request()

                # add to next batch
                elements_in_batch.append(element)
                tokens_in_batch += next_tokens

        # collect any remaining elements into one last request
        add_batched_request()
        return requests

    async def async_get_embeddings(self, series):
        """Get the embeddings for an input data series"""
        # batch the requests
        requests = self._create_request_batches(series)

        # process the batched requests
        responses = await process_api_requests(requests)

        # get the embeddings from the responses
        embeddings = [response.embeddings for response in responses]

        # flatten them
        result = list(itertools.chain.from_iterable(embeddings))

        # convert to series
        result = np.array(result).T.tolist()
        return pd.Series(result)

    def get_function(self):
        def get_embeddings(series):
            nest_asyncio.apply()
            return asyncio.run(self.async_get_embeddings(series))

        return get_embeddings
