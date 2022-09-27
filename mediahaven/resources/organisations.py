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

class Organisations(BaseResource):
    """Public API endpoint of MediaHaven tenants."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = "organisations"

    def get(
        self, organisation: str, accept_format=DEFAULT_ACCEPT_FORMAT,
    ) -> MediaHavenSingleObject:
        """Get all organisations.
        Args:
            organisation: The id of an organisation.
            accept_format: The "Accept" request header.
        Returns:
            A single organisation.
        """
        response = self.mh_client._get(
            self._construct_path(organisation),
            accept_format,
        )
        return MediaHavenSingleObjectCreator.create_object(response, accept_format)
    
    def search(
        self, accept_format: str = DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> MediaHavenPageObject:
        """Search all organisations.
        Args:
            query: The search query.
            accept_format: The "Accept" request header.
        Returns:
            A paged result with the organisations.
        """
        response = self.mh_client._get(
            self._construct_path(),
            accept_format,
            **query_params,
        )
        return MediaHavenPageObjectCreator.create_object(
            response, accept_format, self, **query_params
        )