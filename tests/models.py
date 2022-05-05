from requests import Session

from mediahaven.mediahaven import MediaHavenClient
from mediahaven.oauth2 import OAuth2Grant


class OAuth2GrantTest(OAuth2Grant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None
        self.request_token()

    def request_token(self):
        self.token = {
            "refresh_token": "refresh_token",
            "token_type": "bearer",
            "access_token": "access_token",
            "expires_in": 7200,
        }

    def refresh_token(self):
        self.token = {
            "refresh_token": "refresh_token_after_refresh",
            "token_type": "bearer",
            "access_token": "access_token_after_refresh",
            "expires_in": 7200,
        }

    def _get_session(self):
        return Session()


class MediaHavenClientTest(MediaHavenClient):
    def __init__(self):
        super().__init__(
            "https://localhost/", OAuth2GrantTest("https://localhost/", "id", "secret")
        )
