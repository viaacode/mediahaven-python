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

    def get(
        self, record_id: str, accept_format=DEFAULT_ACCEPT_FORMAT
    ) -> Union[str, dict]:
        """Get a single record.

        Args:
            record_id: It can either be a MediaObjectId, FragmentId or RecordId.

        Returns:
            The record.
        """
        return self.mh_client._get(
            resource_path=self._construct_path(record_id),
            accept_format=accept_format,
        )
