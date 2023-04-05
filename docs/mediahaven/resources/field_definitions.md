# FieldDefinitions

[Mediahaven-python Index](../../../README.md#mediahaven-python-index) /
[MediaHaven](../index.md#mediahaven) /
[Resources](./index.md#resources) /
FieldDefinitions

> Auto-generated documentation for [mediahaven.resources.field_definitions](../../../mediahaven/resources/field_definitions.py) module.

- [FieldDefinitions](#fielddefinitions)
  - [FieldDefinitions](#fielddefinitions-1)
    - [FieldDefinitions().get](#fielddefinitions()get)
    - [FieldDefinitions().search](#fielddefinitions()search)

## FieldDefinitions

[Show source in field_definitions.py:15](../../../mediahaven/resources/field_definitions.py#L15)

Public API endpoint of MediaHaven field definitions.

#### Signature

```python
class FieldDefinitions(BaseResource):
    def __init__(self, *args, **kwargs):
        ...
```

#### See also

- [BaseResource](./base_resource.md#baseresource)

### FieldDefinitions().get

[Show source in field_definitions.py:22](../../../mediahaven/resources/field_definitions.py#L22)

Get a single field definition.

#### Arguments

- `field` - The id or FlatKey of a metadata field definition.
- `accept_format` - The "Accept" request header.

#### Returns

A single metadata field definition.

#### Signature

```python
def get(
    self, field: str = None, accept_format=DEFAULT_ACCEPT_FORMAT
) -> MediaHavenSingleObject:
    ...
```

#### See also

- [DEFAULT_ACCEPT_FORMAT](../mediahaven.md#default_accept_format)
- [MediaHavenSingleObject](./base_resource.md#mediahavensingleobject)

### FieldDefinitions().search

[Show source in field_definitions.py:41](../../../mediahaven/resources/field_definitions.py#L41)

Search all field definitions.

#### Arguments

- `accept_format` - The "Accept" request header.
- `**query_params` - The optional query paramaters:
    - `query_params["startIndex"]` - Used for pagination of search results,
        search results will be returned starting from this index.
    - `query_params["nrOfResults"]` - the number of results that will be returned.
    - `query_params["nested"]` - If true include children and parents in the response,
        default is false.
    - `query_params["sort"]` - Determine how to sort the field definitions. (FieldDefinitionId or LongTranslation).

#### Returns

A paged result with the metadata field definitions.

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