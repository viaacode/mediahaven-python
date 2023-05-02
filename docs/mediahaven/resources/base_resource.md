# BaseResource

[Mediahaven-python Index](../../README.md#mediahaven-python-index) /
[MediaHaven](../index.md#mediahaven) /
[Resources](./index.md#resources) /
BaseResource

> Auto-generated documentation for [mediahaven.resources.base_resource](../../../mediahaven/resources/base_resource.py) module.

- [BaseResource](#baseresource)
  - [BaseResource](#baseresource-1)
    - [BaseResource().mh_client](#baseresource()mh_client)
    - [BaseResource().name](#baseresource()name)
  - [MediaHavenPageObject](#mediahavenpageobject)
    - [MediaHavenPageObject().as_generator](#mediahavenpageobject()as_generator)
    - [MediaHavenPageObject().has_more](#mediahavenpageobject()has_more)
    - [MediaHavenPageObject().next_page](#mediahavenpageobject()next_page)
    - [MediaHavenPageObject().nr_of_results](#mediahavenpageobject()nr_of_results)
    - [MediaHavenPageObject().page_result](#mediahavenpageobject()page_result)
    - [MediaHavenPageObject().raw_response](#mediahavenpageobject()raw_response)
    - [MediaHavenPageObject().start_index](#mediahavenpageobject()start_index)
    - [MediaHavenPageObject().total_nr_of_results](#mediahavenpageobject()total_nr_of_results)
  - [MediaHavenPageObjectCreator](#mediahavenpageobjectcreator)
    - [MediaHavenPageObjectCreator.create_object](#mediahavenpageobjectcreatorcreate_object)
  - [MediaHavenPageObjectJSON](#mediahavenpageobjectjson)
    - [MediaHavenPageObjectJSON().as_generator](#mediahavenpageobjectjson()as_generator)
    - [MediaHavenPageObjectJSON().next_page](#mediahavenpageobjectjson()next_page)
  - [MediaHavenSingleObject](#mediahavensingleobject)
    - [MediaHavenSingleObject().raw_response](#mediahavensingleobject()raw_response)
    - [MediaHavenSingleObject().single_result](#mediahavensingleobject()single_result)
  - [MediaHavenSingleObjectCreator](#mediahavensingleobjectcreator)
    - [MediaHavenSingleObjectCreator.create_object](#mediahavensingleobjectcreatorcreate_object)
  - [MediaHavenSingleObjectJSON](#mediahavensingleobjectjson)
  - [NoMorePagesException](#nomorepagesexception)

## BaseResource

[Show source in base_resource.py:13](../../../mediahaven/resources/base_resource.py#L13)

Base API endpoint of a MediaHaven resource.

#### Attributes

- `_mh_client` - The MediaHaven client used to execute requests.
- `_name` - The name of the resource.

#### Signature

```python
class BaseResource:
    def __init__(self, mh_client: MediaHavenClient):
        ...
```

#### See also

- [MediaHavenClient](../mediahaven.md#mediahavenclient)

### BaseResource().mh_client

[Show source in base_resource.py:34](../../../mediahaven/resources/base_resource.py#L34)

#### Signature

```python
@property
def mh_client(self):
    ...
```

### BaseResource().name

[Show source in base_resource.py:30](../../../mediahaven/resources/base_resource.py#L30)

#### Signature

```python
@property
def name(self):
    ...
```



## MediaHavenPageObject

[Show source in base_resource.py:125](../../../mediahaven/resources/base_resource.py#L125)

Represents a paged result.

As this is a paged result, other pages could be available. The resource which
executed the request together with query parameters are passed as arguments in
other to potentially execute subsequent page requests.

#### Attributes

- `_start_index` - The start index of the executed search request.
- `_nr_of_results` - The number of results of the search result.
- `_total_nr_of_results` - The total number of results of search request.
- `_has_more` - Indicating if there are more pages left.
- `_resource` - The resource that executed the request.
- `_query_params` - The query parameters used in the request.
- `_raw_response` - The raw body of the response.
- `_page_result` - The payload of the response transformed depending on the type.

#### Signature

```python
class MediaHavenPageObject(ABC):
    def __init__(self, response: Response, resource: BaseResource, **query_params):
        ...
```

#### See also

- [BaseResource](#baseresource)

### MediaHavenPageObject().as_generator

[Show source in base_resource.py:172](../../../mediahaven/resources/base_resource.py#L172)

Returns a generator for all the result items spread over all the pages.

#### Returns

A generator.

#### Signature

```python
@abstractmethod
def as_generator(self) -> Generator[Union[SimpleNamespace, str], None, None]:
    ...
```

### MediaHavenPageObject().has_more

[Show source in base_resource.py:185](../../../mediahaven/resources/base_resource.py#L185)

#### Signature

```python
@property
def has_more(self):
    ...
```

### MediaHavenPageObject().next_page

[Show source in base_resource.py:160](../../../mediahaven/resources/base_resource.py#L160)

Fetches the next page.

#### Returns

The next page.

#### Raises

NoMorePagesException if there are no pages left.

#### Signature

```python
@abstractmethod
def next_page(self) -> MediaHavenPageObject:
    ...
```

### MediaHavenPageObject().nr_of_results

[Show source in base_resource.py:189](../../../mediahaven/resources/base_resource.py#L189)

#### Signature

```python
@property
def nr_of_results(self):
    ...
```

### MediaHavenPageObject().page_result

[Show source in base_resource.py:181](../../../mediahaven/resources/base_resource.py#L181)

#### Signature

```python
@property
def page_result(self):
    ...
```

### MediaHavenPageObject().raw_response

[Show source in base_resource.py:201](../../../mediahaven/resources/base_resource.py#L201)

#### Signature

```python
@property
def raw_response(self):
    ...
```

### MediaHavenPageObject().start_index

[Show source in base_resource.py:197](../../../mediahaven/resources/base_resource.py#L197)

#### Signature

```python
@property
def start_index(self):
    ...
```

### MediaHavenPageObject().total_nr_of_results

[Show source in base_resource.py:193](../../../mediahaven/resources/base_resource.py#L193)

#### Signature

```python
@property
def total_nr_of_results(self):
    ...
```



## MediaHavenPageObjectCreator

[Show source in base_resource.py:243](../../../mediahaven/resources/base_resource.py#L243)

Factory class for creating an object which is a subclass of MediaHavenPageObject.

#### Signature

```python
class MediaHavenPageObjectCreator:
    ...
```

### MediaHavenPageObjectCreator.create_object

[Show source in base_resource.py:246](../../../mediahaven/resources/base_resource.py#L246)

Create a MediaHavenPageObject.

As this is a paged result, other pages could be available. The resource which
executed the request together with query parameters are passed as arguments in
other to potentially execute subsequent page requests.

#### Arguments

- `response` - The HTTP response.
- `accept_format` - To determine the format of the result (XML/JSON).
- `resource` - The resource that executed the initial request.
- `**query_params` - The optional query parameters.

#### Returns

The MediaHavenPageObject.

#### Raises

- `NotImplementedError` - When passing an XML format.

#### Signature

```python
@staticmethod
def create_object(
    response: Response,
    accept_format: AcceptFormat,
    resource: BaseResource,
    **query_params
) -> MediaHavenPageObject:
    ...
```

#### See also

- [AcceptFormat](../mediahaven.md#acceptformat)
- [BaseResource](#baseresource)
- [MediaHavenPageObject](#mediahavenpageobject)



## MediaHavenPageObjectJSON

[Show source in base_resource.py:206](../../../mediahaven/resources/base_resource.py#L206)

#### Signature

```python
class MediaHavenPageObjectJSON(MediaHavenPageObject):
    def __init__(self, response: Response, resource: BaseResource, **query_params):
        ...
```

#### See also

- [BaseResource](#baseresource)
- [MediaHavenPageObject](#mediahavenpageobject)

### MediaHavenPageObjectJSON().as_generator

[Show source in base_resource.py:231](../../../mediahaven/resources/base_resource.py#L231)

#### Signature

```python
def as_generator(self) -> Generator[SimpleNamespace, None, None]:
    ...
```

### MediaHavenPageObjectJSON().next_page

[Show source in base_resource.py:223](../../../mediahaven/resources/base_resource.py#L223)

#### Signature

```python
def next_page(self) -> MediaHavenPageObjectJSON:
    ...
```



## MediaHavenSingleObject

[Show source in base_resource.py:61](../../../mediahaven/resources/base_resource.py#L61)

Represents a single result.

#### Attributes

- `_raw_response` - The raw body of the response.
- `_single_result` - The payload of the response transformed depending on the type.

#### Signature

```python
class MediaHavenSingleObject(ABC):
    def __init__(self, response: Response):
        ...
```

### MediaHavenSingleObject().raw_response

[Show source in base_resource.py:82](../../../mediahaven/resources/base_resource.py#L82)

#### Signature

```python
@property
def raw_response(self):
    ...
```

### MediaHavenSingleObject().single_result

[Show source in base_resource.py:78](../../../mediahaven/resources/base_resource.py#L78)

#### Signature

```python
@property
def single_result(self):
    ...
```



## MediaHavenSingleObjectCreator

[Show source in base_resource.py:98](../../../mediahaven/resources/base_resource.py#L98)

Factory class for creating an object which is a subclass of MediaHavenSingleObject.

#### Signature

```python
class MediaHavenSingleObjectCreator:
    ...
```

### MediaHavenSingleObjectCreator.create_object

[Show source in base_resource.py:101](../../../mediahaven/resources/base_resource.py#L101)

Create a MediaHavenSingleObject.

#### Arguments

- `response` - The HTTP response.

#### Returns

The MediaHavenSingleObject.

#### Raises

- `NotImplementedError` - When passing an XML format.

#### Signature

```python
@staticmethod
def create_object(
    response: Response, accept_format: AcceptFormat
) -> MediaHavenSingleObject:
    ...
```

#### See also

- [AcceptFormat](../mediahaven.md#acceptformat)
- [MediaHavenSingleObject](#mediahavensingleobject)



## MediaHavenSingleObjectJSON

[Show source in base_resource.py:87](../../../mediahaven/resources/base_resource.py#L87)

#### Signature

```python
class MediaHavenSingleObjectJSON(MediaHavenSingleObject):
    def __init__(self, response: Response):
        ...
```

#### See also

- [MediaHavenSingleObject](#mediahavensingleobject)



## NoMorePagesException

[Show source in base_resource.py:120](../../../mediahaven/resources/base_resource.py#L120)

#### Signature

```python
class NoMorePagesException(Exception):
    def __init__(self):
        ...
```