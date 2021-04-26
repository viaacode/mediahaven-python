#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Union

from mediahaven.mediahaven import DEFAULT_ACCEPT_FORMAT
from mediahaven.resources.base_resource import BaseResource


class Records(BaseResource):
    """Public API endpoint of a MediaHaven record."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "records"

    def count(self, query: str) -> int:
        """Counts the amount the records given a query string.

        Args:
            query: Free text search string.

        Returns:
            The amount of records.
        """
        return self.mh_client._head(
            resource_path=self._construct_path(),
            q=query,
        )

    def get(
        self, record_id: str, accept_format=DEFAULT_ACCEPT_FORMAT
    ) -> Union[str, dict]:
        """Get a single record.

        Args:
            record_id: It can either be a MediaObjectId, FragmentId or RecordId.
            accept_format: The "Accept" request header

        Returns:
            The record.
        """
        return self.mh_client._get(
            self._construct_path(record_id),
            accept_format,
        )

    def search(
        self, query: str, accept_format=DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> Union[str, dict]:
        """Query multiple records given a query string.

        Args:
            query: Free text search string.
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: the number of results that will be returned
        Returns:
            A paged result with the records.
        """
        return self.mh_client._get(
            self._construct_path(),
            accept_format,
            q=query,
            **query_params,
        )

    def list(
        self, accept_format=DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> Union[str, dict]:
        """list the records.

        Args:
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: the number of results that will be returned
        Returns:
            A paged result with the records.
        """
        return self.mh_client._get(
            self._construct_path(),
            accept_format,
            **query_params,
        )

    def delete(self, record_id: str, reason: str = None, event_type: str = None):
        """Delete a record.

        Args:
            record_id: The ID of the record to remove.
                It can be either a MediaObjectId, FragmentId or RecordId.
            reason: The reason to delete the record.
            event_type: A custom subtype for the delete event.
        """

        # Construct the optional body
        body = {}
        if reason:
            body["reason"] = reason
        if event_type:
            body["event_type"] = event_type

        return self.mh_client._delete(
            resource_path=self._construct_path(record_id),
            **body,
        )
