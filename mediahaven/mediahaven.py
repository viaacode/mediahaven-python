#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from typing import Optional, Union

from requests import RequestException
from requests.exceptions import JSONDecodeError
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
from mediahaven.retry import RetryException, retry_exponential, TooManyRetriesException

API_PATH = "/mediahaven-rest-api/v2/"


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


class ContentType(Enum):
    JSON = "application/json"
    XML = "application/xml"


DEFAULT_ACCEPT_FORMAT = AcceptFormat.JSON


class MediaHavenClient:
    """The MediaHaven client class to communicate with MediaHaven.

    Attributes:
        - grant: The OAuth2.0 grant.
        - mh_base_url: The MediaHaven base URL (https://{host}:{port}).
        - mh_api_url: The mh_base_url concatenated with the API path including the version.
        - retry_rate_limit: Indicates if when hitting a rate limit, the request should be retried.
    """

    def __init__(
        self, mh_base_url: str, grant: OAuth2Grant, retry_rate_limit: bool = False
    ):
        """Initialize a MediaHaven client.

        Args:
            - mh_base_url:  The MediaHaven base URL (https://{host}:{port}).
            - grant: The OAuth2.0 grant.
            - retry_rate_limit: Indicates if, when hitting a rate limit, the request should be retried.
        """
        self.grant = grant
        self.mh_base_url = mh_base_url
        self.mh_api_url = urljoin(self.mh_base_url, API_PATH)
        self.retry_rate_limit = retry_rate_limit

    def _raise_mediahaven_exception_if_needed(self, response):
        """Raise a MediaHaven exception if the response status >= 400.

        Args:
            The response.

        Raises:
            MediaHavenException wrapping the response error.
        """

        if response.status_code >= 400:
            try:
                error_message = response.json()
            except ValueError:
                error_message = {"response": response.text}
            raise MediaHavenException(error_message, status_code=response.status_code)

    @retry_exponential((RetryException), 1, 2, 10)
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
            requests.RequestException: Reraise if a RequestException happen.
            TooManyRetriesException: If all the (re)tries have been exhausted.
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
                session = self.grant._get_session()
                response = session.request(**kwargs)
            except InvalidGrantError:
                # Refresh token invalid / revoked
                # Depending on grant, different action is needed
                raise RefreshTokenError
            else:
                return response
        except RequestException:
            raise
        except TooManyRetriesException:
            raise
        else:
            if self.retry_rate_limit and response.status_code == 429:
                raise RetryException
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
        resource_url = urljoin(self.mh_api_url, resource_path)

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
        resource_url = urljoin(self.mh_api_url, resource_path)

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
        resource_url = urljoin(self.mh_api_url, resource_path)

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
        self,
        resource_path: str,
        json: dict = None,
        xml: str = None,
        files: dict = None,
        **form_data,
    ) -> Union[dict, bool]:
        """Execute a POST request.

        For some POST requests, MediaHaven allows JSON, XML or multipart/form-data.
        Only one of the options is allowed. If multiple options are passed a
        ValueError will be raised.

        Args:
            resource_path: The path of the resource.
            json: The JSON payload.
            xml: The XML payload.
            files: The files to upload. This is only used if form-data is used.
            **form_data: The form data.

        Returns:
            - The requests response as a dict if the status code is in the successful
                2xx range and the response contains a body.
            - True if the status code is in the successful 2xx range but no response
                body.
            - False if the status code is not in the successful 2xx range but also
                not in error range (4xx-5xx).

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
        resource_url = urljoin(self.mh_api_url, resource_path)

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
            # Execute the request - Form
            files = files if files else {}
            response = self._execute_request(
                **dict(method="POST", url=resource_url, files=files, data=form_data)
            )

        # Raise appropriate exception if HTTPError occurred
        self._raise_mediahaven_exception_if_needed(response)

        # Parse response information
        if response.status_code in (range(200, 207)):
            try:
                return response.json()
            except JSONDecodeError:
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
        resource_url = urljoin(self.mh_api_url, resource_path)

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
