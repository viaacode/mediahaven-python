#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mediahaven.mediahaven import MediaHavenClient


class BaseResource:
    """Base API endpoint of a MediaHaven resource."""

    def __init__(self, mh_client: MediaHavenClient):
        """Initialize a resource.

        Args:
            mh_client: The MediaHaven client.
        """
        self.mh_client = mh_client
        self.name = ""

    def _construct_path(self, *path_segments) -> str:
        """Construct the path of the request URL.

        The path segments are joined together by a "/". Those segments are then prefixed
        with the resource name, with a "/" in between.

        Example:
            Given the resource name "records" and the path_segments: (1,profiles,1).
            The constructed path is: "records/1/profiles/1".

        Args:
            *paths: Variable list of path segments.

        Returns:
            The constructed path of the request URL.
        """
        suffix = "/".join(map(str, path_segments))
        return f"{self.name}/{suffix}"
