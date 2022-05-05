import pytest
from unittest.mock import patch

from mediahaven.resources.base_resource import AcceptFormat
from mediahaven.resources.records import Records


class TestRecords:
    @pytest.fixture()
    def records(self, mh_client_mock):
        return Records(mh_client_mock)

    @patch("mediahaven.resources.records.MediaHavenSingleObjectCreator")
    def test_get(self, object_creator_mock, records: Records):
        # Arrange
        media_id = "1"
        mh_client_mock = records.mh_client

        # Act
        records.get(media_id)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{records.name}/{media_id}", AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON
        )

    @patch("mediahaven.resources.records.MediaHavenPageObjectCreator")
    def test_search(self, object_creator_mock, records: Records):
        # Arrange
        media_id = "1"
        mh_client_mock = records.mh_client

        query = f'(MediaObjectId:"{media_id}")'

        # Act
        records.search(q=query)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            records.name, AcceptFormat.JSON, q='(MediaObjectId:"1")'
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON, records, q='(MediaObjectId:"1")'
        )

    def test_count(self, records: Records):
        # Arrange
        media_id = "1"
        query = f'(MediaObjectId:"{media_id}")'

        # Act
        records.count(query)

        # Assert
        records.mh_client._head.assert_called_once_with(records.name, q=query)

    def test_delete(self, records: Records):
        # Arrange
        media_id = "1"
        payload = {"reason": "reason", "event_type": "subtype"}

        # Act
        records.delete(media_id, **payload)

        # Assert
        records.mh_client._delete.assert_called_once_with(
            f"{records.name}/{media_id}", Reason="reason", EventType="subtype"
        )

    def test_update_json(self, records: Records):
        # Arrange
        media_id = "1"
        payload = {"description": "New description"}

        # Act
        resp = records.update(media_id, json=payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{media_id}", json=payload, xml=None
        )

    def test_update_xml(self, records: Records):
        # Arrange
        media_id = "1"
        payload = "<description>New description</description>"

        # Act
        resp = records.update(media_id, xml=payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{media_id}", json=None, xml=payload
        )

    def test_update_form_data(self, records: Records):

        # Arrange
        media_id = "1"
        payload = {"description": "New description"}

        # Act
        resp = records.update(media_id, **payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{media_id}", json=None, xml=None, **payload
        )
