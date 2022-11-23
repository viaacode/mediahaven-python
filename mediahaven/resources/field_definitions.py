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
    """Public API endpoint of MediaHaven field definitions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = "field-definitions"

    def get(
        self,
        field: str = None,
        accept_format=DEFAULT_ACCEPT_FORMAT,
    ) -> MediaHavenSingleObject:
        """Get a single field definition.

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
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: the number of results that will be returned.
                query_params["nested"]: If true include children and parents in the response,
                    default is false.
                query_params["sort"]: Determine how to sort the field definitions. (FieldDefinitionId or LongTranslation).
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
