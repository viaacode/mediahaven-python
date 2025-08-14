# Records

[Mediahaven-python Index](../../README.md#mediahaven-python-index) /
[MediaHaven](../index.md#mediahaven) /
[Resources](./index.md#resources) /
Records

> Auto-generated documentation for [mediahaven.resources.records](../../../mediahaven/resources/records.py) module.

- [Records](#records)
  - [Records](#records-1)
    - [Records().count](#records()count)
    - [Records().delete](#records()delete)
    - [Records().get](#records()get)
    - [Records().publish](#records()publish)
    - [Records().search](#records()search)
    - [Records().update](#records()update)

## Records

[Show source in records.py:15](../../../mediahaven/resources/records.py#L15)

Public API endpoint of a MediaHaven record.

#### Signature

```python
class Records(BaseResource):
    def __init__(self, *args, **kwargs):
        ...
```

#### See also

- [BaseResource](./base_resource.md#baseresource)

### Records().count

[Show source in records.py:22](../../../mediahaven/resources/records.py#L22)

Counts the amount the records given a query string.

#### Arguments

- `query` - Free text search string.

#### Returns

The amount of records.

#### Signature

```python
def count(self, query: str) -> int:
    ...
```

### Records().delete

[Show source in records.py:81](../../../mediahaven/resources/records.py#L81)

Delete a record.

#### Arguments

- `record_id` - The ID of the record to remove.
    It can be either a MediaObjectId, FragmentId or RecordId.
- `reason` - The reason to delete the record.
- `event_type` - A custom subtype for the delete event.

#### Signature

```python
def delete(self, record_id: str, reason: str = None, event_type: str = None):
    ...
```

### Records().get

[Show source in records.py:36](../../../mediahaven/resources/records.py#L36)

Get a single record.

#### Arguments

- `record_id` - It can either be a MediaObjectId, FragmentId or RecordId.
- `accept_format` - The "Accept" request header.

#### Returns

A single record.

#### Signature

```python
def get(
    self, record_id: str, accept_format=DEFAULT_ACCEPT_FORMAT
) -> MediaHavenSingleObject:
    ...
```

#### See also

- [DEFAULT_ACCEPT_FORMAT](../mediahaven.md#default_accept_format)
- [MediaHavenSingleObject](./base_resource.md#mediahavensingleobject)

### Records().publish

[Show source in records.py:121](../../../mediahaven/resources/records.py#L121)

Publishes a record.

#### Arguments

- `record_id` - The ID of the record to publish.
    It can be either a MediaObjectId, FragmentId or RecordId.
- `reason` - The reason to publish the record.

#### Signature

```python
def publish(self, record_id: str, reason: str = None):
    ...
```

### Records().search

[Show source in records.py:54](../../../mediahaven/resources/records.py#L54)

Search for multiple records.

#### Arguments

- `accept_format` - The "Accept" request header.
- `**query_params` - The optional query paramaters:
    - `query_params["q"]` - Free text search string.
    - `query_params["startIndex"]` - Used for pagination of search results,
        search results will be returned starting from this index.
    - `query_params["nrOfResults"]` - The number of results that will be returned.
    - `query_params["publicOnly"]` - If true exclude from the output dynamic
        metadata fields which were marked as non public in the Profiles
        linked with the record.

#### Returns

A paged result with the records.

#### Signature

```python
def search(
    self, accept_format=DEFAULT_ACCEPT_FORMAT, **query_params
) -> MediaHavenPageObject:
    ...
```

#### See also

- [DEFAULT_ACCEPT_FORMAT](../mediahaven.md#default_accept_format)
- [MediaHavenPageObject](./base_resource.md#mediahavenpageobject)

### Records().update

[Show source in records.py:103](../../../mediahaven/resources/records.py#L103)

Update a record.

#### Arguments

- `record_id` - The ID of the record to remove.
    It can be either a MediaObjectId, FragmentId or RecordId.
- `json` - The JSON payload.
- `xml` - The XML payload.
- `**form_data` - The payload as multipart/form-data.

#### Signature

```python
def update(self, record_id: str, json: dict = None, xml: str = None, **form_data):
    ...
```