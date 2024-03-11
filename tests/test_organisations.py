import pytest
from unittest.mock import patch

from mediahaven.resources.base_resource import AcceptFormat
from mediahaven.resources.organisations import Organisations

class TestOrganisations:
    @pytest.fixture()
    def organisations(self, mh_client_mock):
        return Organisations(mh_client_mock)

    @patch("mediahaven.resources.organisations.MediaHavenSingleObjectCreator")
    def test_get(self, object_creator_mock, organisations: Organisations):
        # Arrange
        organisation_id = "1"
        mh_client_mock = organisations.mh_client

        # Act
        organisations.get(organisation_id)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{organisations.name}/{organisation_id}", AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON
        )
    
    @patch("mediahaven.resources.organisations.MediaHavenSingleObjectCreator")
    def test_get_by_external_id(self, object_creator_mock, organisations: Organisations):
        # Arrange
        external_id = "OR-a11111a"
        mh_client_mock = organisations.mh_client

        # Act
        organisations.get_by_external_id(external_id)

        # Assert
        mh_client_mock._get.assert_called_once_with(
            f"{organisations.name}/ExternalId:{external_id}", AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON
        )
    
    @patch("mediahaven.resources.organisations.MediaHavenPageObjectCreator")
    def test_search(self, object_creator_mock, organisations: Organisations):
        # Arrange
        mh_client_mock = organisations.mh_client

        # Act
        organisations.search()

        # Assert
        mh_client_mock._get.assert_called_once_with(
            organisations.name, AcceptFormat.JSON
        )
        object_creator_mock.create_object.assert_called_once_with(
            mh_client_mock._get(), AcceptFormat.JSON, organisations
        )