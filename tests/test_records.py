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
        record_id = "1"
        mh_client_mock = records.mh_client

        # Act
        records.get(record_id)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{records.name}/{record_id}", AcceptFormat.JSON
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
        record_id = "1"
        payload = {"reason": "reason", "event_type": "subtype"}

        # Act
        records.delete(record_id, **payload)

        # Assert
        records.mh_client._delete.assert_called_once_with(
            f"{records.name}/{record_id}", Reason="reason", EventType="subtype"
        )

    def test_update_json(self, records: Records):
        # Arrange
        record_id = "1"
        payload = {"description": "New description"}

        # Act
        resp = records.update(record_id, json=payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{record_id}", json=payload, xml=None
        )

    def test_update_xml(self, records: Records):
        # Arrange
        record_id = "1"
        payload = "<description>New description</description>"

        # Act
        resp = records.update(record_id, xml=payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{record_id}", json=None, xml=payload
        )

    def test_update_form_data(self, records: Records):
        # Arrange
        record_id = "1"
        payload = {"description": "New description"}

        # Act
        resp = records.update(record_id, **payload)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{record_id}", json=None, xml=None, **payload
        )

    def test_publish_without_reason(self, records: Records):
        # Arrange
        record_id = "1"
        body = {"Publish": True}

        # Act
        resp = records.publish(record_id)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{record_id}", json=body
        )

    def test_publish_with_reason(self, records: Records):
        # Arrange
        record_id = "1"
        reason = "test"
        body = {"Reason": reason, "Publish": True}

        # Act
        resp = records.publish(record_id, reason)

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            f"{records.name}/{record_id}", json=body
        )

    def test_create_fragment_time_codes(self, records: Records):
        # Arrange
        record_id = "1"
        title = "Title"
        start_time_code = "00:01:00.000"
        end_time_code = "00:02:00.000"

        # Act
        resp = records.create_fragment(
            record_id,
            title,
            start_time_code=start_time_code,
            end_time_code=end_time_code,
        )

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            "records",
            json={
                "Title": "Title",
                "Type": "fragment",
                "Publish": True,
                "Fragment": {
                    "ParentRecordId": "1",
                    "FragmentStartTimeCode": "00:01:00.000",
                    "FragmentEndTimeCode": "00:02:00.000",
                },
            },
        )

    def test_create_fragment_frames(self, records: Records):
        # Arrange
        record_id = "1"
        title = "Title"
        start_frames = 5
        end_frames = 10
        # Act
        resp = records.create_fragment(
            record_id, title, start_frames=start_frames, end_frames=end_frames
        )

        # Assert
        resp == records.mh_client._post.return_value
        records.mh_client._post.assert_called_once_with(
            "records",
            json={
                "Title": "Title",
                "Type": "fragment",
                "Publish": True,
                "Fragment": {
                    "ParentRecordId": "1",
                    "FragmentStartFrames": 5,
                    "FragmentEndFrames": 10,
                },
            },
        )

    def test_create_fragment_value_error_no_values(self, records: Records):
        # Arrange
        record_id = "1"
        title = "Title"

        # Act
        with pytest.raises(ValueError) as error:
            records.create_fragment(record_id, title)

        # Assert
        assert (
            str(error.value)
            == "Provide either a combination of start_time_code and end_time_code or start_frames and end_frames."
        )

    def test_create_fragment_value_mixed(self, records: Records):
        # Arrange
        record_id = "1"
        title = "Title"
        start_time_code = "00:01:00.000"
        end_frames = 5

        # Act
        with pytest.raises(ValueError) as error:
            records.create_fragment(
                record_id, title, start_time_code=start_time_code, end_frames=end_frames
            )

        # Assert
        assert (
            str(error.value)
            == "Provide either a combination of start_time_code and end_time_code or start_frames and end_frames."
        )

    def test_create_fragment_value_incomplete(self, records: Records):
        # Arrange
        record_id = "1"
        title = "Title"
        start_time_code = "00:01:00.000"

        # Act
        with pytest.raises(ValueError) as error:
            records.create_fragment(record_id, title, start_time_code=start_time_code)

        # Assert
        assert (
            str(error.value)
            == "Provide either a combination of start_time_code and end_time_code or start_frames and end_frames."
        )
