import pytest
from unittest.mock import patch

from mediahaven.resources.base_resource import AcceptFormat
from mediahaven.resources.fields import Fields

class TestFields:
    @pytest.fixture()
    def fields(self, mh_client_mock):
        return Fields(mh_client_mock)

    @patch("mediahaven.resources.fields.MediaHavenSingleObjectCreator")
    def test_get(self, object_creator_mock, fields: Fields):
        # Arrange
        field_flat_key = "Title"
        mh_client_mock = fields.mh_client

        # Act
        fields.get(field_flat_key)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{fields.name}/{field_flat_key}", AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON
        )
    @patch("mediahaven.resources.fields.MediaHavenPageObjectCreator")
    def test_get_all(self, object_creator_mock, fields: Fields):
        # Arrange
        mh_client_mock = fields.mh_client

        # Act
        fields.get()

        # Assert
        mh_client_mock._get.assert_called_once_with(
            fields.name, AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON, fields
        )
