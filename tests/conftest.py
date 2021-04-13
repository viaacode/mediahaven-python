import pytest

from tests.models import MediaHavenClientTest


@pytest.fixture(scope="package")
def mh_client():
    return MediaHavenClientTest()
