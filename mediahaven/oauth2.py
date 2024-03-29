#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from urllib.parse import urljoin

from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2.rfc6749.errors import (
    CustomOAuth2Error,
    InvalidClientError,
)
from requests_oauthlib import OAuth2Session


class RequestTokenError(Exception):
    """Raised when an error occurred during token request.

    Abstracts the underlying OAuthlib2 errors.
    """

    def __init__(self):
        super().__init__("Error occurred when requesting a token.")


class RefreshTokenError(Exception):
    """Raised when an error occurred during token request.

    Abstracts the underlying OAuthlib2 errors.
    """

    def __init__(self):
        super().__init__("Error occurred when refreshing a token.")


class NoTokenError(Exception):
    """Raised when a token has not been requested yet."""

    def __init__(self):
        super().__init__("Authorized access is needed. Request a token first.")


class OAuth2Grant(ABC):
    """Abstract class representing an OAuth2 grant used in MediaHaven."""

    def __init__(self, mh_base_url: str, client_id: str, client_secret: str):
        """Initialize a Grant class.

        Args:
            mh_base_url: The URL of MH auth server.
            client_id: The ID of the client.
            client_secret: The secret of the client.
        """
        self.mh_base_url = mh_base_url
        self.client = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.refresh_url = urljoin(self.mh_base_url, "/auth/oauth2/token")

    @abstractmethod
    def request_token(self):
        pass

    def refresh_token(self):
        """Refresh the OAuth2 token with the saved refresh token.

        Issues a new access token but also a new refresh token.
        """
        # Create a session containing the (refresh) token
        oauth = OAuth2Session(client=self.client, token=self.token)
        # These extra params are needed to refresh the token
        extra = {"client_id": self.client_id, "client_secret": self.client_secret}
        # Refresh the token
        self.token = oauth.refresh_token(self.refresh_url, **extra)

    def _get_session(self) -> OAuth2Session:
        """Return a requests session with the valid OAuth2 token.

        This session can be used to execute the authorized requests. This means that
        a token needs to have been requested before getting this session.

        Returns:
            A session with the valid OAuth2 token.

        Raises:
            MissingTokenError: When a token has not yet been requested.
        """
        if not self.token:
            raise NoTokenError
        return OAuth2Session(client=self.client, token=self.token)


class ROPCGrant(OAuth2Grant):
    """Represents a "Resource Owner Password Credential" grant."""

    def __init__(self, mh_base_url: str, client_id: str, client_secret: str):
        super().__init__(mh_base_url, client_id, client_secret)
        self.token_url = urljoin(self.mh_base_url, "/auth/ropc.php")
        self.client = LegacyApplicationClient(self.client_id)

    def request_token(self, username: str, password: str):
        """Request an OAuth2 token.

        The resource owner grants the client the authorization to execute the
        requests on its behalf. Given the credentials of the resource owner, an auth
        token is issued by the authorization server. This token will be saved in memory
        and used by the session in order to execute authorized requests.

        Args:
            username: The username of the resource owner.
            password: The password of the resource owner.

        Raises:
            RequestTokenException: When an error occurred when requesting the token.
        """
        # Create a session to request the token
        oauth = OAuth2Session(client=self.client)

        # Fetch the access token
        try:
            self.token = oauth.fetch_token(
                token_url=self.token_url,
                username=username,
                password=password,
                client_id=self.client_id,
                client_secret=self.client_secret,
                include_client_id=True,
            )
        except (CustomOAuth2Error, InvalidClientError) as err:
            raise RequestTokenError from err
