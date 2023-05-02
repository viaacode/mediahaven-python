# Mediahaven

[Mediahaven-python Index](../README.md#mediahaven-python-index) /
[MediaHaven](./index.md#mediahaven) /
Mediahaven

> Auto-generated documentation for [mediahaven.mediahaven](../../mediahaven/mediahaven.py) module.

- [Mediahaven](#mediahaven)
  - [AcceptFormat](#acceptformat)
  - [MediaHavenClient](#mediahavenclient)
  - [MediaHavenException](#mediahavenexception)

## AcceptFormat

[Show source in mediahaven.py:31](../../mediahaven/mediahaven.py#L31)

#### Signature

```python
class AcceptFormat(Enum):
    ...
```



## MediaHavenClient

[Show source in mediahaven.py:42](../../mediahaven/mediahaven.py#L42)

The MediaHaven client class to communicate with MediaHaven.

#### Signature

```python
class MediaHavenClient:
    def __init__(self, mh_base_url: str, grant: OAuth2Grant):
        ...
```

#### See also

- [OAuth2Grant](./oauth2.md#oauth2grant)



## MediaHavenException

[Show source in mediahaven.py:25](../../mediahaven/mediahaven.py#L25)

#### Signature

```python
class MediaHavenException(Exception):
    def __init__(self, message: str, status_code: int = None):
        ...
```