#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Union

from mediahaven.mediahaven import DEFAULT_ACCEPT_FORMAT
from mediahaven.resources.base_resource import BaseResource


class Records(BaseResource):
    """Public API endpoint of a MediaHaven record."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "records"

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
    ) -> Union[List[str], List[dict]]:
        """Query multiple records.

        Args:
            query: Free text search string.
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: the number of results that will be returned
        Returns:
            The records.
        """
        return self.mh_client._get(
            self._construct_path(),
            accept_format,
            q=query,
            **query_params,
        )
