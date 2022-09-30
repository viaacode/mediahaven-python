import pytest
from unittest.mock import patch

from mediahaven.resources.base_resource import AcceptFormat
from mediahaven.resources.field_definitions import FieldDefinitions

class TestFields:
    @pytest.fixture()
    def field_definitions(self, mh_client_mock):
        return FieldDefinitions(mh_client_mock)

    @patch("mediahaven.resources.field_definitions.MediaHavenSingleObjectCreator")
    def test_get(self, object_creator_mock, field_definitions: FieldDefinitions):
        # Arrange
        field_flat_key = "Title"
        mh_client_mock = field_definitions.mh_client

        # Act
        field_definitions.get(field_flat_key)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{field_definitions.name}/{field_flat_key}", AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON
        )
        
    @patch("mediahaven.resources.field_definitions.MediaHavenPageObjectCreator")
    def test_search(self, object_creator_mock, field_definitions: FieldDefinitions):
        # Arrange
        mh_client_mock = field_definitions.mh_client

        # Act
        field_definitions.search()

        # Assert
        mh_client_mock._get.assert_called_once_with(
            field_definitions.name, AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON, field_definitions
        )
