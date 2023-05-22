#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict
from mediahaven.mediahaven import DEFAULT_ACCEPT_FORMAT
from mediahaven.resources.base_resource import (
    BaseResource,
    MediaHavenPageObject,
    MediaHavenPageObjectCreator,
    MediaHavenSingleObject,
    MediaHavenSingleObjectCreator,
)


class Records(BaseResource):
    """Public API endpoint of a MediaHaven record."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = "records"

    def count(self, query: str) -> int:
        """Counts the amount the records given a query string.

        Args:
            query: Free text search string.

        Returns:
            The amount of records.
        """
        return self.mh_client._head(
            self._construct_path(),
            q=query,
        )

    def get(
        self, record_id: str, accept_format=DEFAULT_ACCEPT_FORMAT
    ) -> MediaHavenSingleObject:
        """Get a single record.

        Args:
            record_id: It can either be a MediaObjectId, FragmentId or RecordId.
            accept_format: The "Accept" request header.

        Returns:
            A single record.
        """
        response = self.mh_client._get(
            self._construct_path(record_id),
            accept_format,
        )
        return MediaHavenSingleObjectCreator.create_object(response, accept_format)

    def search(
        self, accept_format=DEFAULT_ACCEPT_FORMAT, **query_params
    ) -> MediaHavenPageObject:
        """Search for multiple records.

        Args:
            accept_format: The "Accept" request header.
            **query_params: The optional query paramaters:
                query_params["q"]: Free text search string.
                query_params["startIndex"]: Used for pagination of search results,
                    search results will be returned starting from this index.
                query_params["nrOfResults"]: The number of results that will be returned.
                query_params["publicOnly"]: If true exclude from the output dynamic
                    metadata fields which were marked as non public in the Profiles
                    linked with the record.
        Returns:
            A paged result with the records.
        """
        response = self.mh_client._get(
            self._construct_path(),
            accept_format,
            **query_params,
        )
        return MediaHavenPageObjectCreator.create_object(
            response, accept_format, self, **query_params
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
            body["Reason"] = reason
        if event_type:
            body["EventType"] = event_type

        return self.mh_client._delete(
            self._construct_path(record_id),
            **body,
        )

    def update(self, record_id: str, json: dict = None, xml: str = None, **form_data):
        """Update a record.

        Args:
            record_id: The ID of the record to remove.
                It can be either a MediaObjectId, FragmentId or RecordId.
            json: The JSON payload.
            xml: The XML payload.
            **form_data: The payload as multipart/form-data.
        """

        return self.mh_client._post(
            self._construct_path(record_id),
            json=json,
            xml=xml,
            **form_data,
        )

    def publish(self, record_id: str, reason: str = None):
        """Publishes a record.

        Args:
            record_id: The ID of the record to publish.
                It can be either a MediaObjectId, FragmentId or RecordId.
            reason: The reason to publish the record.
        """
        # Construct the body
        body: Dict[str, Any] = {}
        if reason:
            body["Reason"] = reason

        body["Publish"] = True

        return self.mh_client._post(self._construct_path(record_id), json=body)

    def create_fragment(
        self,
        record_id: str,
        title: str,
        start_time_code=None,
        end_time_code=None,
        start_frames=None,
        end_frames=None,
    ):
        """Create a fragment for an existing record.

        Args:
            record_id: The ID of the record to create a fragment for.
                It needs to be the RecordId.
            title: The title of the fragment object.
            start_time_code: The start time code of the fragment.
            end_time_code: The end time code of the fragment.
            start_frames: The start time of the fragment in frames.
            end_frames: The end time of the fragment in frames.

        Raises:
            ValueError: Start and end time need to be provided. They can be provided
                as timecodes or as frames. However, only one set can be provided, and
                one set needs to contain both start and end values. In any other case,
                raise a ValueError.
        """
        # Build the JSON
        json = {
            "Title": title,
            "Type": "fragment",
            "Publish": True,
            "Fragment": {"ParentRecordId": record_id},
        }

        # Add the timecodes or frames
        if (start_time_code or end_time_code) and (start_frames or end_frames):
            raise ValueError(
                "Provide either a combination of start_time_code and end_time_code or start_frames and end_frames."
            )
        elif start_time_code and end_time_code:
            json["Fragment"]["FragmentStartTimeCode"] = start_time_code
            json["Fragment"]["FragmentEndTimeCode"] = end_time_code
        elif start_frames and end_frames:
            json["Fragment"]["FragmentStartFrames"] = start_frames
            json["Fragment"]["FragmentEndFrames"] = end_frames
        else:
            raise ValueError(
                "Provide either a combination of start_time_code and end_time_code or start_frames and end_frames."
            )

        return self.mh_client._post(
            self._construct_path(),
            json=json,
        )
