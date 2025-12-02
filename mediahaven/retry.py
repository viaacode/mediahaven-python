import functools
import time


class RetryException(Exception):
    """Exception raised when an action needs to be retried
    in combination with retry_exponential decorator"""

    pass


class TooManyRetriesException(Exception):
    """Exception raised when all the tries are exhausted"""

    pass


DELAY = 1
BACKOFF = 2
NUMBER_OF_TRIES = 10


def retry_exponential(
    exceptions: list[BaseException],
    delay_seconds: int = DELAY,
    backoff: int = BACKOFF,
    number_of_tries: int = NUMBER_OF_TRIES,
):
    """A decorator allowing for a function to be retried via an exponential backoff

    Raises:
     - TooManyRetriesException: When all the (re)tries are exhausted.
    """

    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            number_of_tries_over = number_of_tries
            delay = delay_seconds
            while number_of_tries_over:
                number_of_tries_over -= 1
                try:
                    return func(self, *args, **kwargs)
                except exceptions as error:
                    # Todo: log
                    time.sleep(delay)
                    delay *= backoff
            raise TooManyRetriesException(f"Too many retries: {number_of_tries}")

        return wrapper

    return decorator_retry
