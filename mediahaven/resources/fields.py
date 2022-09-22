#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from mediahaven.mediahaven import DEFAULT_ACCEPT_FORMAT
from mediahaven.resources.base_resource import (
    BaseResource,
    MediaHavenPageObject,
    MediaHavenPageObjectCreator,
    MediaHavenSingleObject,
    MediaHavenSingleObjectCreator,
)


class Fields(BaseResource):
    """Public API endpoint of MediaHaven metadata fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = "field-definitions"

    def get(
        self, field: str=None, accept_format=DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> Union[MediaHavenSingleObject, MediaHavenPageObject]:
        """Get all field definitions.

        Args:
            field: The id or FlatKey of a metadata field definition.
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: the number of results that will be returned
                query_params["nested"]: Include children and parents in the response.
                query_params["sort"]: Determine how to sort the field definitions	
        Returns:
            If field is None: 
                A paged result with the metadata field definitions.
            If field is not None:
                A single metadata field definition.
        """
        if field:
            response = self.mh_client._get(
            self._construct_path(field),
            accept_format,
            )
            return MediaHavenSingleObjectCreator.create_object(response, accept_format)
        else:
            response = self.mh_client._get(
                self._construct_path(),
                accept_format,
                **query_params,
            )
            return MediaHavenPageObjectCreator.create_object(
                response, accept_format, self, **query_params
            )
