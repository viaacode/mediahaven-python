#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import Generator, Optional, Union

from requests.models import Response

from mediahaven.mediahaven import AcceptFormat, MediaHavenClient


class BaseResource:
    """Base API endpoint of a MediaHaven resource.

    Attributes:
        _mh_client: The MediaHaven client used to execute requests.
        _name: The name of the resource.
    """

    def __init__(self, mh_client: MediaHavenClient):
        """Initialize a resource.

        Args:
            mh_client: The MediaHaven client.
        """
        self._mh_client = mh_client
        self._name = ""

    @property
    def name(self):
        return self._name

    def _construct_path(self, *path_segments) -> str:
        """Construct the path of the request URL.

        The path segments are joined together by a "/". Those segments are then prefixed
        with the resource name, with a "/" in between.

        Example:
            Given the resource name "records" and the path_segments: (1,profiles,1).
            The constructed path is: "records/1/profiles/1".

        If there are no path_segments, just the resource name is returned. Without
        a trailing slash.

        Args:
            *paths: Variable list of path segments.

        Returns:
            The constructed path of the request URL.
        """
        suffix = "/".join(map(str, path_segments))
        return f"{self.name}/{suffix}" if suffix else self.name


class MediaHavenSingleObject(ABC):
    """Represents a single result.

    Attributes:
        _raw_response: The raw body of the response.
        _single_result: The payload of the response transformed depending on the type.
    """

    def __init__(self, response: Response):
        """Initializes a MediaHavenSingleObject.

        Args:
            response: The HTTP response.
        """
        self._raw_response: str = response.text
        self._single_result: Optional[Union[SimpleNamespace, str]] = None

    @property
    def single_result(self):
        return self._single_result


class MediaHavenSingleObjectJSON(MediaHavenSingleObject):
    def __init__(self, response: Response):
        super().__init__(response)
        self._single_result: SimpleNamespace = response.json(
            object_hook=lambda d: SimpleNamespace(**d)
        )


class MediaHavenSingleObjectCreator:
    """Factory class for creating an object which is a subclass of MediaHavenSingleObject."""

    @staticmethod
    def create_object(
        response: Response, accept_format: AcceptFormat
    ) -> MediaHavenSingleObject:
        """Create a MediaHavenSingleObject.

        Args:
            response: The HTTP response.
        Returns:
            The MediaHavenSingleObject.
        Raises:
            NotImplementedError: When passing an XML format.
        """
        if accept_format == AcceptFormat.JSON:
            return MediaHavenSingleObject(response)
        else:
            raise NotImplementedError("XML format is not yet implemented")


class MediaHavenPageObject(ABC):
    """Represents a paged result.

    As this is a paged result, other pages could be available. The resource which
    executed the request together with query parameters are passed as arguments in
    other to potentially execute subsequent page requests.

    Attributes:
        _start_index: The start index of the executed search request.
        _nr_of_results: The number of results of the search result.
        _total_nr_of_results: The total number of results of search request.
        _has_more: Indicating if there are more pages left.
        _resource: The resource that executed the request.
        _query_params: The query parameters used in the request.
        _raw_response: The raw body of the response.
        _page_result: The payload of the response transformed depending on the type.
    """

    def __init__(self, response: Response, resource: BaseResource, **query_params):
        """Initializes a MediaHavenPageObject.

        Args:
            response: The HTTP response.
            resource: The resource that executed the initial request.
            **query_params: The optional query paramaters.
        """
        self._resource: BaseResource = resource
        self._query_params: dict = query_params
        self._raw_response: str = response.text
        self._start_index: Optional[int] = None
        self._nr_of_results: Optional[int] = None
        self._total_nr_of_results: Optional[int] = None
        self._has_more: Optional[bool] = None
        self._page_result: Optional[Union[SimpleNamespace, str]] = None

    @abstractmethod
    def as_generator(self) -> Generator[Union[SimpleNamespace, str], None, None]:
        """Returns a generator for all the result items spread over all the pages.

        Returns:
            A generator.
        """
        pass

    @property
    def page_result(self):
        return self._page_result

    @property
    def has_more(self):
        return self._has_more

    @property
    def nr_of_results(self):
        return self._nr_of_results

    @property
    def total_nr_of_results(self):
        return self._total_nr_of_results

    @property
    def start_index(self):
        return self._start_index


class MediaHavenPageObjectJSON(MediaHavenPageObject):
    def __init__(self, response: Response, resource: BaseResource, **query_params):
        """Initializes a MediaHavenPageObjectJSON."""
        super().__init__(response, resource, **query_params)

        self._page_result = response.json(object_hook=lambda d: SimpleNamespace(**d))
        self._total_nr_of_results = self.page_result.TotalNrOfResults
        self._nr_of_results = self.page_result.NrOfResults
        self._start_index = self.page_result.StartIndex

        self._has_more = self.total_nr_of_results > (
            self.nr_of_results + self.start_index
        )

    def __getitem__(self, key):
        return self.page_result.Results[key]

    def as_generator(self) -> Generator[SimpleNamespace, None, None]:
        page = self
        while True:
            for result in page.page_result.Results:
                yield result

            if page.has_more:
                # Fetch next page
                params = page._query_params.copy()
                params["StartIndex"] = page.start_index + page.nr_of_results
                page = page._resource.search(accept_format=AcceptFormat.JSON, **params)
            else:
                break


class MediaHavenPageObjectCreator:
    """Factory class for creating an object which is a subclass of MediaHavenPageObject."""

    @staticmethod
    def create_object(
        response: Response,
        accept_format: AcceptFormat,
        resource: BaseResource,
        **query_params,
    ) -> MediaHavenPageObject:
        """Create a MediaHavenPageObject.

        As this is a paged result, other pages could be available. The resource which
        executed the request together with query parameters are passed as arguments in
        other to potentially execute subsequent page requests.

        Args:
            response: The HTTP response.
            accept_format: To determine the format of the result (XML/JSON).
            resource: The resource that executed the initial request.
            **query_params: The optional query parameters.
        Returns:
            The MediaHavenPageObject.
        Raises:
            NotImplementedError: When passing an XML format.
        """
        if accept_format == AcceptFormat.JSON:
            return MediaHavenPageObjectJSON(response, resource, **query_params)
        else:
            raise NotImplementedError("XML format is not yet implemented")
