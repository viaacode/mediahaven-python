from pathlib import Path

import pytest

from mediahaven.mocks.base_resource import (
    MediaHavenPageObjectJSONMock,
    MediaHavenSingleObjectJSONMock,
    MediaHavenSingleObjectXMLMock,
)


def test_media_haven_single_object_json_mock():
    data = {"Dynamic": {"field": "value"}}
    single_object_mock = MediaHavenSingleObjectJSONMock(data)
    assert single_object_mock.Dynamic.field == "value"


def test_media_haven_page_object_json_mock():
    data = [{"Dynamic": {"field": "value"}}]
    page_object_mock = MediaHavenPageObjectJSONMock(
        data, nr_of_results=5, total_nr_of_results=10, start_index=3
    )
    assert page_object_mock[0].Dynamic.field == "value"
    assert page_object_mock.nr_of_results == 5
    assert page_object_mock.total_nr_of_results == 10
    assert page_object_mock.start_index == 3


@pytest.fixture
def mh_single_object_xml():
    return Path("tests", "resources", "mh_single_object.xml").read_text()


def test_media_haven_single_object_xml_mock(mh_single_object_xml):
    single_object_mock = MediaHavenSingleObjectXMLMock(mh_single_object_xml)
    assert single_object_mock.single_result == mh_single_object_xml
