from unittest.mock import MagicMock, patch
from mediahaven.retry import (
    retry_exponential,
    RetryException,
    TooManyRetriesException,
    NUMBER_OF_TRIES,
    DELAY,
    BACKOFF,
)
import pytest


@patch("time.sleep")
def test_retry_defaults(time_sleep_mock):
    function_mock = MagicMock()
    function_mock.side_effect = RetryException

    @retry_exponential((RetryException))
    def func(self):
        function_mock()

    # Execute the decorated method
    with pytest.raises(TooManyRetriesException):
        func(MagicMock())

    # Test if function was executed multiple times
    assert function_mock.call_count == NUMBER_OF_TRIES

    # Test if time.sleep was executed multiple times
    assert time_sleep_mock.call_count == NUMBER_OF_TRIES

    # Test exponential backoff
    assert time_sleep_mock.call_args_list[0][0][0] == DELAY
    for i in range(1, NUMBER_OF_TRIES):
        prev_val = time_sleep_mock.call_args_list[i - 1][0][0]
        assert time_sleep_mock.call_args_list[i][0][0] == prev_val * BACKOFF


@patch("time.sleep")
def test_retry(time_sleep_mock):
    function_mock = MagicMock()
    function_mock.side_effect = RetryException

    @retry_exponential((RetryException), 2, 4, 5)
    def func(self):
        function_mock()

    # Execute the decorated method
    with pytest.raises(TooManyRetriesException):
        func(MagicMock())

    # Test if function was executed multiple times
    assert function_mock.call_count == 5

    # Test if time.sleep was executed multiple times
    assert time_sleep_mock.call_count == 5

    # Test exponential backoff
    assert time_sleep_mock.call_args_list[0][0][0] == 2
    for i in range(1, 5):
        prev_val = time_sleep_mock.call_args_list[i - 1][0][0]
        assert time_sleep_mock.call_args_list[i][0][0] == prev_val * 4
