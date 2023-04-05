# Oauth2

[Mediahaven-python Index](../../README.md#mediahaven-python-index) /
[MediaHaven](./index.md#mediahaven) /
Oauth2

> Auto-generated documentation for [mediahaven.oauth2](../../mediahaven/oauth2.py) module.

- [Oauth2](#oauth2)
  - [NoTokenError](#notokenerror)
  - [OAuth2Grant](#oauth2grant)
    - [OAuth2Grant().refresh_token](#oauth2grant()refresh_token)
    - [OAuth2Grant().request_token](#oauth2grant()request_token)
  - [ROPCGrant](#ropcgrant)
    - [ROPCGrant().request_token](#ropcgrant()request_token)
  - [RefreshTokenError](#refreshtokenerror)
  - [RequestTokenError](#requesttokenerror)

## NoTokenError

[Show source in oauth2.py:38](../../mediahaven/oauth2.py#L38)

Raised when a token has not been requested yet.

#### Signature

```python
class NoTokenError(Exception):
    def __init__(self):
        ...
```



## OAuth2Grant

[Show source in oauth2.py:45](../../mediahaven/oauth2.py#L45)

Abstract class representing an OAuth2 grant used in MediaHaven.

#### Signature

```python
class OAuth2Grant(ABC):
    def __init__(self, mh_base_url: str, client_id: str, client_secret: str):
        ...
```

### OAuth2Grant().refresh_token

[Show source in oauth2.py:67](../../mediahaven/oauth2.py#L67)

Refresh the OAuth2 token with the saved refresh token.

Issues a new access token but also a new refresh token.

#### Signature

```python
def refresh_token(self):
    ...
```

### OAuth2Grant().request_token

[Show source in oauth2.py:63](../../mediahaven/oauth2.py#L63)

#### Signature

```python
@abstractmethod
def request_token(self):
    ...
```



## ROPCGrant

[Show source in oauth2.py:96](../../mediahaven/oauth2.py#L96)

Represents a "Resource Owner Password Credential" grant.

#### Signature

```python
class ROPCGrant(OAuth2Grant):
    def __init__(self, mh_base_url: str, client_id: str, client_secret: str):
        ...
```

#### See also

- [OAuth2Grant](#oauth2grant)

### ROPCGrant().request_token

[Show source in oauth2.py:104](../../mediahaven/oauth2.py#L104)

Request an OAuth2 token.

The resource owner grants the client the authorization to execute the
requests on its behalf. Given the credentials of the resource owner, an auth
token is issued by the authorization server. This token will be saved in memory
and used by the session in order to execute authorized requests.

#### Arguments

- `username` - The username of the resource owner.
- `password` - The password of the resource owner.

#### Raises

- `RequestTokenException` - When an error occurred when requesting the token.

#### Signature

```python
def request_token(self, username: str, password: str):
    ...
```



## RefreshTokenError

[Show source in oauth2.py:28](../../mediahaven/oauth2.py#L28)

Raised when an error occurred during token request.

Abstracts the underlying OAuthlib2 errors.

#### Signature

```python
class RefreshTokenError(Exception):
    def __init__(self):
        ...
```



## RequestTokenError

[Show source in oauth2.py:18](../../mediahaven/oauth2.py#L18)

Raised when an error occurred during token request.

Abstracts the underlying OAuthlib2 errors.

#### Signature

```python
class RequestTokenError(Exception):
    def __init__(self):
        ...
```