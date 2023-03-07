# Adapted from
# https://github.com/openai/openai-cookbook/blob/66b988407d8d13cad5060a881dc8c892141f2d5c/examples/api_request_parallel_processor.py

"""
API REQUESTER

Using the OpenAI API to process lots of text quickly takes some care.
If you trickle in a million API requests one by one, they'll take days to complete.
If you flood a million API requests in parallel, they'll exceed the rate limits and fail with errors.
To maximize throughput, parallel requests need to be throttled to stay under rate limits.

This script parallelizes requests to the OpenAI API while throttling to stay under rate limits.

Features:
- Makes requests concurrently, to maximize throughput
- Throttles request and token usage, to stay under rate limits
- Retries failed requests up to {max_attempts} times, to avoid missing data
- Logs errors, to diagnose problems with requests

Inputs:
- requests_list : List[OpenAIRequest[T]]
    - a list of requests to process
- max_requests_per_minute : float, optional
    - target number of requests to make per minute (will make less if limited by tokens)
    - leave headroom by setting this to 50% or 75% of your limit
    - if requests are limiting you, try batching multiple embeddings or completions into one request
    - if omitted, will default to 1,500
- max_tokens_per_minute : float, optional
    - target number of tokens to use per minute (will use less if limited by requests)
    - leave headroom by setting this to 50% or 75% of your limit
    - if omitted, will default to 125,000
- max_attempts : int, optional
    - number of times to retry a failed request before giving up
    - if omitted, will default to 5

The script is structured as follows:
    - Imports
    - Define process_api_requests()
        - Initialize things
        - In main loop:
            - Get next request if one is not already waiting for capacity
            - Update available token & request capacity
            - If enough capacity available, call API
            - The loop pauses if a rate limit error is hit
            - The loop breaks when no tasks remain
    - Define dataclasses
        - StatusTracker (stores script metadata counters; only one instance is created)
        - RetryableRequest (stores API inputs, outputs, metadata; one method to call API)
    - Define functions
        - task_id_generator_function (yields 1, 2, 3, ...)
"""

# imports
import asyncio  # for running API calls concurrently
import logging  # for logging rate limit warnings and other messages
import time  # for sleeping after rate limit is hit
from dataclasses import dataclass
from typing import Generic, List

from nlp_primitives.openai.request import RESPONSE, OpenAIRequest
from openai.error import OpenAIError, RateLimitError


async def process_api_requests(
    request_list: List[OpenAIRequest[RESPONSE]],
    max_requests_per_minute: float = 3_000 * 0.5,
    max_tokens_per_minute: float = 250_000 * 0.5,
    max_attempts: int = 5,
    seconds_to_pause_after_rate_limit_error: int = 15,
    seconds_to_sleep_each_loop: float = 0.001,  # 1 ms limits max throughput to 1,000 requests per second
) -> List[RESPONSE]:
    """Processes API requests in parallel, throttling to stay under rate limits."""
    logging.debug("Initializing requester.")

    # initialize trackers
    queue_of_requests_to_retry = asyncio.Queue()
    request_id_generator = (
        request_id_generator_function()
    )  # generates integer IDs of 1, 2, 3, ...
    status_tracker = (
        StatusTracker()
    )  # single instance to track a collection of variables
    next_request = None  # variable to hold the next request to run

    # initialize available capacity counts
    available_request_capacity = max_requests_per_minute
    available_token_capacity = max_tokens_per_minute
    last_update_time = time.time()

    # initialize flags
    requests_remaining = True
    logging.debug("Initialization complete.")

    # `requests` will provide requests one at a time
    requests = request_list.__iter__()
    logging.debug("Iteration started. Entering main loop")

    sent_requests = []
    while True:
        # get next task (if one is not already waiting for capacity)
        if next_request is None:
            if queue_of_requests_to_retry.empty() is False:
                next_request = queue_of_requests_to_retry.get_nowait()
                logging.debug(
                    f"Retrying request {next_request.request_id}: {next_request}"
                )
            elif requests_remaining:
                try:
                    # get new request
                    request = next(requests)
                    next_request = RetryableRequest(
                        request_id=next(request_id_generator),
                        request=request,
                        attempts_left=max_attempts,
                    )
                    sent_requests.append(next_request)
                    status_tracker.num_tasks_started += 1
                    status_tracker.num_tasks_in_progress += 1
                    logging.debug(
                        f"Created request {next_request.request_id}: {next_request}"
                    )
                except StopIteration:
                    # if requests list runs out, set flag to stop iterating
                    logging.debug("Requests list exhausted")
                    requests_remaining = False

        # update available capacity
        current_time = time.time()
        seconds_since_update = current_time - last_update_time
        available_request_capacity = min(
            available_request_capacity
            + max_requests_per_minute * seconds_since_update / 60.0,
            max_requests_per_minute,
        )
        available_token_capacity = min(
            available_token_capacity
            + max_tokens_per_minute * seconds_since_update / 60.0,
            max_tokens_per_minute,
        )
        last_update_time = current_time

        # if enough capacity available, call API
        if next_request:
            next_request_tokens = next_request.request.token_consumption
            if (
                available_request_capacity >= 1
                and available_token_capacity >= next_request_tokens
            ):
                # update counters
                available_request_capacity -= 1
                available_token_capacity -= next_request_tokens
                next_request.attempts_left -= 1

                # call API
                asyncio.create_task(
                    next_request.execute(
                        retry_queue=queue_of_requests_to_retry,
                        status_tracker=status_tracker,
                    )
                )
                next_request = None  # reset next_request to empty

        # if all tasks are finished, break
        if status_tracker.num_tasks_in_progress == 0:
            break

        # main loop sleeps briefly so concurrent tasks can run
        await asyncio.sleep(seconds_to_sleep_each_loop)

        # if a rate limit error was hit recently, pause to cool down
        seconds_since_rate_limit_error = (
            time.time() - status_tracker.time_of_last_rate_limit_error
        )
        if seconds_since_rate_limit_error < seconds_to_pause_after_rate_limit_error:
            remaining_seconds_to_pause = (
                seconds_to_pause_after_rate_limit_error - seconds_since_rate_limit_error
            )
            await asyncio.sleep(remaining_seconds_to_pause)
            # ^e.g., if pause is 15 seconds and final limit was hit 5 seconds ago
            until = time.ctime(
                status_tracker.time_of_last_rate_limit_error
                + seconds_to_pause_after_rate_limit_error
            )
            logging.warning(f"Pausing to cool down until {until}")

    # after finishing, log final status
    logging.info("""Parallel processing complete.""")
    if status_tracker.num_rate_limit_errors > 0:
        logging.warning(
            f"{status_tracker.num_rate_limit_errors} rate limit errors received."
            " Consider running at a lower rate."
        )

    return [req.response for req in sent_requests]


# dataclasses


@dataclass
class StatusTracker:
    """Stores metadata about the script's progress. Only one instance is created."""

    num_tasks_started: int = 0
    num_tasks_in_progress: int = 0  # script ends when this reaches 0
    num_tasks_succeeded: int = 0
    num_rate_limit_errors: int = 0
    time_of_last_rate_limit_error: int = 0  # used to cool off after hitting rate limits


@dataclass
class RetryableRequest(Generic[RESPONSE]):
    """Stores an API request's inputs, outputs, and other metadata. Contains a method to make an API call.
    """

    request_id: int
    request: OpenAIRequest
    attempts_left: int
    errors = []
    response: RESPONSE | None = None

    async def execute(
        self,
        retry_queue: asyncio.Queue,
        status_tracker: StatusTracker,
    ):
        """Calls the OpenAI API and saves results."""
        logging.info(f"Starting request #{self.request_id}")
        error = None
        try:
            self.response = await self.request.execute()
        except RateLimitError:
            status_tracker.time_of_last_rate_limit_error = time.time()
            status_tracker.num_rate_limit_errors += 1
        except OpenAIError as e:
            logging.warning(f"Request {self.request_id} failed with Exception {e}")
            error = e

        if error:
            self.errors.append(error)
            if self.attempts_left:
                retry_queue.put_nowait(self)
            else:
                logging.error(
                    f"Request {self.request_id} failed after all attempts:"
                    f" {self.errors}"
                )
                status_tracker.num_tasks_in_progress -= 1
                raise error
        else:
            logging.debug(f"Request {self.request_id} succeeded")
            status_tracker.num_tasks_in_progress -= 1
            status_tracker.num_tasks_succeeded += 1


def request_id_generator_function():
    """Generate integers 0, 1, 2, and so on."""
    request_id = 0
    while True:
        yield request_id
        request_id += 1
