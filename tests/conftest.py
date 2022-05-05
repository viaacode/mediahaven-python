from unittest.mock import MagicMock
import pytest

from tests.models import MediaHavenClientTest


@pytest.fixture()
def mh_client():
    return MediaHavenClientTest()


@pytest.fixture()
def mh_client_mock():
    return MagicMock()
