#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from enum import Enum
from typing import Optional

from requests import RequestException
from requests.models import Response

from oauthlib.oauth2.rfc6749.errors import (
    TokenExpiredError,
    InvalidGrantError,
)
from urllib.parse import urlencode, urljoin, quote as urlquote

from mediahaven.oauth2 import (
    NoTokenError,
    OAuth2Grant,
    RefreshTokenError,
)

MH_BASE_URL = os.environ["MH_BASE_URL"]
API_PATH = "mediahaven-rest-api/v2/"


class MediaHavenException(Exception):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class AcceptFormat(Enum):
    JSON = "application/json"
    XML = "application/xml"
    DUBLIN = "application/dc+xml"
    METS = "application/mets+mhs+xml"
    UNKNOWN = ""


DEFAULT_ACCEPT_FORMAT = AcceptFormat.JSON


class MediaHavenClient:
    """The MediaHaven client class to communicate with MediaHaven."""

    def __init__(self, grant: OAuth2Grant):
        self.grant = grant
        self.base_url_path = f"{MH_BASE_URL}{API_PATH}"

    def _raise_mediahaven_exception_if_needed(self, response):
        """Raise a MediaHaven exception if the response status >= 400.

        Args:
            The response.

        Raises:
            A MediaHavenException wrapping the response error.
        """

        if response.status_code >= 400:
            try:
                error_message = response.json()
            except ValueError:
                error_message = {"response": response.text}
            raise MediaHavenException(error_message, status_code=response.status_code)

    def _execute_request(self, **kwargs):
        """Execute an authorized request.

        In order to do so, a token needs to have been requested at this point.

        If the token is expired, a new token will be issued via the refresh token.
        If it is not possible to refresh the token for example due to an expired
        refresh token, raise a RefreshTokenError as manual action is required.

        Args:
            **kwargs: the kwargs to pass to the request.
        Returns:
            The response object.
        Raises:
            NoTokenError: If a token has not yet been requested.
            RefreshTokenError: If an error occurred when refreshing the token.
        """
        # Get a session with a valid auth
        try:
            session = self.grant._get_session()
        except NoTokenError:
            raise

        # Execute request
        try:
            response = session.request(**kwargs)
        except TokenExpiredError:
            # There is a token but expired, try to refresh the token.
            try:
                self.grant.refresh_token()
                self.grant._get_session()
                response = session.request(**kwargs)
            except InvalidGrantError:
                # Refresh token invalid / revoked
                # Depending on grant, different action is needed
                raise RefreshTokenError
        except RequestException:
            # TODO: Log/raise?
            pass
        else:
            return response

    def _build_headers(self, accept_format: AcceptFormat = None) -> dict:
        headers = {}
        if accept_format:
            headers["Accept"] = accept_format.value

        return headers

    def _encode_query_params(self, **query_params) -> Optional[str]:
        """Encode the query parameters.

        Encode the spaces in the query parameters as "%20" and not "+".

        Returns:
            The encoded query parameters.
        """
        params = urlencode(query_params, quote_via=urlquote) if query_params else None
        return params

    def _head(self, resource_path: str, **query_params) -> int:
        """Execute a HEAD request and return the result information.

        A HEAD operation returns the amount of items of the resource in the header
        of the response with the name "Result-Count".

        Args:
            resource_path: The path of the resource.
            **query_params: The query string parameters.

        Returns:
            The amount of items.

        Raises:
            MediaHavenException: If the response has a status >= 400.
        """
        # The resource URL up until path
        resource_url = urljoin(self.base_url_path, resource_path)

        # Get the query parameters in MH specific encoding
        params = self._encode_query_params(**query_params)

        # Construct the request headers
        headers = self._build_headers()

        # Execute the request
        response = self._execute_request(
            **dict(method="HEAD", url=resource_url, headers=headers, params=params)
        )

        # Raise appropriate exception if HTTPError occurred
        self._raise_mediahaven_exception_if_needed(response)

        # Parse response information
        return int(response.headers["Result-Count"])

    def _get(
        self, resource_path: str, accept_format: AcceptFormat, **query_params
    ) -> Response:
        """Execute a GET request and return the HTTP response.

        Args:
            resource_path: The path of the resource.
            accept_format: The "Accept" request header.
            **query_params: The query string parameters.

        Returns:
            The HTTP response.

        Raises:
            MediaHavenException: If the response has a status >= 400.
        """
        # The resource URL including the path
        resource_url = urljoin(self.base_url_path, resource_path)

        # Encode the query parameters in a MH specific encoding
        params = self._encode_query_params(**query_params)

        # Construct the request headers
        headers = self._build_headers(accept_format)

        # Execute the request
        response = self._execute_request(
            **dict(method="GET", url=resource_url, headers=headers, params=params)
        )

        # Raise exception if the response state code >= 400
        self._raise_mediahaven_exception_if_needed(response)

        # Return response
        return response

    def _delete(self, resource_path: str, **body) -> bool:
        """Execute a DELETE request.

        Args:
            resource_path: The path of the resource.
            **body: The optional request body.

        Returns:
            True if successful.

        Raises:
            MediaHavenException: If the response has a status >= 400.
        """
        # The resource URL up until path
        resource_url = urljoin(self.base_url_path, resource_path)

        # Execute the request
        response = self._execute_request(
            **dict(method="DELETE", url=resource_url, json=body)
        )

        # Raise appropriate exception if HTTPError occurred
        self._raise_mediahaven_exception_if_needed(response)

        # Parse response information
        if response.status_code == 204:
            return True

        return False

    def _post(
        self, resource_path: str, json: dict = None, xml: str = None, **form_data
    ) -> bool:
        """Execute a POST request.

        For some POST requests, MediaHaven allows JSON, XML or multipart/form-data.
        Only one of the options is allowed. If multiple options are passed a
        ValueError will be raised.

        Args:
            resource_path: The path of the resource.
            json: The JSON payload.
            xml: The XML payload.
            **form_data: The payload as multipart/form-data.

        Returns:
            True if successful.

        Raises:
            MediaHavenException: If the response has a status >= 400.
            ValueError: If multiple payload values are passed (json, xml or form_data).
        """
        # Check if only one payload value is passed
        if bool(json) + bool(xml) + bool(form_data) != 1:
            raise ValueError(
                "Only one payload value is allowed (json, xml or form_data)"
            )
        # The resource URL up until path
        resource_url = urljoin(self.base_url_path, resource_path)

        # Depending on the type of payload a different request should be send
        if json:
            # Execute the request
            response = self._execute_request(
                **dict(method="POST", url=resource_url, json=json)
            )
        elif xml:
            headers = {"content-type": "application/xml"}
            # Execute the request
            response = self._execute_request(
                **dict(method="POST", url=resource_url, headers=headers, data=xml)
            )
        else:
            # Execute the request - Multipart/form-data
            response = self._execute_request(
                **dict(method="POST", url=resource_url, files=form_data)
            )

        # Raise appropriate exception if HTTPError occurred
        self._raise_mediahaven_exception_if_needed(response)

        # Parse response information
        if response.status_code in (200, 204):
            return True

        return False

    def _put(
        self, resource_path: str, json: dict = None, xml: str = None, **form_data
    ) -> bool:
        """Execute a PUT request.

        For some PUT requests, MediaHaven allows JSON or XML. Only one of the options
        is allowed. If multiple options are passed a ValueError will be raised.

        Args:
            resource_path: The path of the resource.
            json: The JSON payload.
            xml: The XML payload.

        Returns:
            True if successful.

        Raises:
            MediaHavenException: If the response has a status >= 400.
            ValueError: If multiple payload values are passed (json or xml).
        """
        # Check if only one payload value is passed
        if bool(json) + bool(xml) != 1:
            raise ValueError("Only one payload value is allowed (json or xml)")
        # The resource URL up until path
        resource_url = urljoin(self.base_url_path, resource_path)

        # Depending on the type of payload a different request should be send
        if json:
            # Execute the request
            response = self._execute_request(
                **dict(method="PUT", url=resource_url, json=json)
            )
        elif xml:
            headers = {"content-type": "application/xml"}
            # Execute the request
            response = self._execute_request(
                **dict(method="PUT", url=resource_url, headers=headers, data=xml)
            )

        # Raise appropriate exception if HTTPError occurred
        self._raise_mediahaven_exception_if_needed(response)

        # Parse response information
        if response.status_code in (200, 204):
            return True

        return False
