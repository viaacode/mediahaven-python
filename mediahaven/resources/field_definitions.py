#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from mediahaven.mediahaven import DEFAULT_ACCEPT_FORMAT
from mediahaven.resources.base_resource import (
    BaseResource,
    MediaHavenPageObject,
    MediaHavenPageObjectCreator,
    MediaHavenSingleObject,
    MediaHavenSingleObjectCreator,
)


class FieldDefinitions(BaseResource):
    """Public API endpoint of MediaHaven metadata fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = "field-definitions"

    def get(
        self, field: str=None, accept_format=DEFAULT_ACCEPT_FORMAT,
    ) -> MediaHavenSingleObject:
        """Get all field definitions.

        Args:
            field: The id or FlatKey of a metadata field definition.
            accept_format: The "Accept" request header.
        Returns:
            A single metadata field definition.
        """
        response = self.mh_client._get(
            self._construct_path(field),
            accept_format,
        )
        return MediaHavenSingleObjectCreator.create_object(response, accept_format)

    def search(
        self, accept_format: str = DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> MediaHavenPageObject:
        """Search all field definitions.

        Args:
            query: The search query.
            accept_format: The "Accept" request header.
        Returns:
            A paged result with the metadata field definitions.
        """
        response = self.mh_client._get(
            self._construct_path(),
            accept_format,
            **query_params,
        )
        return MediaHavenPageObjectCreator.create_object(
            response, accept_format, self, **query_params
        )
