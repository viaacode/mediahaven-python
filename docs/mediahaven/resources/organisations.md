# Organisations

[Mediahaven-python Index](../../README.md#mediahaven-python-index) /
[MediaHaven](../index.md#mediahaven) /
[Resources](./index.md#resources) /
Organisations

> Auto-generated documentation for [mediahaven.resources.organisations](../../../mediahaven/resources/organisations.py) module.

- [Organisations](#organisations)
  - [Organisations](#organisations-1)
    - [Organisations().get](#organisations()get)
    - [Organisations().search](#organisations()search)

## Organisations

[Show source in organisations.py:15](../../../mediahaven/resources/organisations.py#L15)

Public API endpoint of MediaHaven tenants.

#### Signature

```python
class Organisations(BaseResource):
    def __init__(self, *args, **kwargs):
        ...
```

#### See also

- [BaseResource](./base_resource.md#baseresource)

### Organisations().get

[Show source in organisations.py:22](../../../mediahaven/resources/organisations.py#L22)

Get a single organisation.

#### Arguments

- `organisation_id` - The id of an organisation.
- `accept_format` - The "Accept" request header.

#### Returns

A single organisation.

#### Signature

```python
def get(
    self, organisation_id: str, accept_format=DEFAULT_ACCEPT_FORMAT
) -> MediaHavenSingleObject:
    ...
```

#### See also

- [DEFAULT_ACCEPT_FORMAT](../mediahaven.md#default_accept_format)
- [MediaHavenSingleObject](./base_resource.md#mediahavensingleobject)

### Organisations().search

[Show source in organisations.py:40](../../../mediahaven/resources/organisations.py#L40)

Search all organisations.

#### Arguments

- `query` - The search query.
- `accept_format` - The "Accept" request header.
- `**query_params` - The optional query parameters:
    - `query_params["startIndex"]` - Used for pagination of search results,
        search results will be returned starting from this index.
    - `query_params["nrOfResults"]` - The number of results that will be returned.

#### Returns

A paged result with the organisations.

#### Signature

```python
def search(
    self, accept_format: str = DEFAULT_ACCEPT_FORMAT, **query_params
) -> MediaHavenPageObject:
    ...
```

#### See also

- [DEFAULT_ACCEPT_FORMAT](../mediahaven.md#default_accept_format)
- [MediaHavenPageObject](./base_resource.md#mediahavenpageobject)