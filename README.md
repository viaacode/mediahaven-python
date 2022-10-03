# MediaHaven Python Library

## Synopsis

The Mediahaven Python library provides a way to communicate with MediaHaven via the v2 REST API.
- [OAuth Client](#mediahavenoauth2)
- [Mediahaven Client](#mediahavenmediahaven)
- Resources
    - [Organisations](#organisations)
    - [Fields](#fields)
    - [Records](#records)
## ```mediahaven.oauth2```
### ```ROPCGrant()```
Parameters:
| Name | Description | Default |
| ---- | ----------- | ------- |
| mh_base_url | the Mediahaven base URL. <br /> ```str``` | *required* |
| client_id | Mediahaven Client id. <br /> ```str``` | *required* |
| client_secret | Mediahaven Client secret. <br /> ```str``` | *required* |

<details>
    <summary>Code example</summary>

```python
>>> import os
>>> from mediahaven.oauth2 import ROPCGrant, RequestTokenError

>>> # Get the credentials from env vars.
>>> client_id = os.environ["CLIENT_ID"]
>>> client_secret = os.environ["CLIENT_SECRET"]
>>> url = os.environ["MH_URL"]

>>> # Create a ROPC grant
>>> grant = ROPCGrant(url, client_id, client_secret)
```

</details>

### ```ROPCGrant.request_token()```
Parameters:
| Name | Description | Default |
| ---- | ----------- | ------- |
| username | Mediahaven username. <br /> ```str``` | *required* |
| password | Mediahaven password. <br /> ```str``` | *required* |


<details>
    <summary>Code example</summary>

```python
>>> import os
>>> from mediahaven.oauth2 import ROPCGrant, RequestTokenError

>>> # Get the credentials from env vars.
>>> username = os.environ["USERNAME"]
>>> password = os.environ["PASSWORD"]
>>> try:
...     grant.request_token(username, password)
... except RequestTokenError as e:
...     print(e)
```

</details>

## ```mediahaven.mediahaven```
### ```Mediahaven()```
Parameters:
| Name | Description | Default |
| ---- | ----------- | ------- |
| mh_base_url | Mediahaven base URL. <br /> ```str``` | *required* |
| grant | OAuth2 Grant client. <br /> [```ROPCGrant```](#ropcgrant) | *required* |

<details>
<summary>Code example</summary>

```python
>>> from mediahaven import MediaHaven

>>> # Initialize the MH client
>>> client = MediaHaven(url, grant)
```

</details>

### Records
### ```Mediahaven.records.get()```
Parameters:
| Name | Description | Default |
| ---- | ----------- | ------- |
| record_id | MediaObjectId, FragmentId or RecordId. <br /> ```str``` | *required* |
| accept_format | The "Accept" request header. <br /> ```AcceptFormat``` <br /> JSON, XML, DUBLIN, METS or UNKOWN | JSON |

Returns:
| Type | Description | 
| ---- | ----------- | 
| ```MediaHavenSingleObject``` | A single record. | 


<details>
<summary>Code example</summary>

```python
>>> from mediahaven import MediaHaven

>>> # Get record based on record ID
>>> record = client.records.get("570...33b")
>>> print(record.Internal.ArchiveStatus)
on_disk
>>> print(record.Dynamic.PID)
qs...8q
```

</details>

### ```Mediahaven.records.search()```
Parameters:
| Name | Description | Default |
| ---- | ----------- | ------- |
| accept_format | The "Accept" request header. <br /> ```AcceptFormat``` <br /> JSON, XML, DUBLIN, METS or UNKOWN | JSON |
| **query_params <br /> <ul> <li>q</li> <li>startIndex</li> <li>nrOfResults</li> <li>publicOnly</li> </ul> | The optional query paramaters. <br /> <ul><li>Free text search string</li><li>Search results will be returned starting from this index.</li><li>Number of results that will be returned.</li><li>If true exclude fields which were marked as non public in the record's Profiles</li></ul> | *optional* |

Returns:
| Type | Description | 
| ---- | ----------- | 
| [```MediaHavenPageObject```](#mediahavenpageobject) | A paged result with the records. | 

<details>
    <summary>Code example</summary>

```python
>>> # Get page based on query
>>> records_page = client.records.search(q="+(batch_id:FLMB15)", nrOfResults=10, startIndex=0)
>>> print(records_page.nr_of_results)
10
>>> print(records_page.total_nr_of_results)
22
>>> print(records_page.start_index)
0
>>> print(records_page[0].Dynamic.PID)
w3...0k
```

</details>

## ```mediahaven.resources.base_resource```

### ```MediahavenSingleObject()```
Represents a single result.



### ```MediahavenPageObject()```
Represents a paged result.
### ```MediahavenPageObject.next_page()```
Fetches the next page.

Returns:
| Type | Description | 
| ---- | ----------- | 
| [```MediahavenPageObject```](#mediahavenpageobject) | The next page. |

<details>
<summary>Code example</summary>

```python
>>> # Get next page
>>> next_page = current_page.next_page()
```

</details>

### ```MediahavenPageObject.as_generator()```
Returns a generator for all the result items spread over all the pages.

Returns:
| Type | Description | 
| ---- | ----------- | 
| ```Generator``` | A generator for all result items. |

<details>
<summary>Code example</summary>

```python
>>> # Work via generator
>>> for record in records_page.as_generator():
...     print(record.Dynamic.PID)
... 
w3...0k
<SNIP 20 IDs>
9s...5t
```

</details>

#### Properties

### ```MediahavenPageObject.has_more```
Returns:
| Type | Description | 
| ---- | ----------- | 
| ```bool``` | A boolean indicating if there are more pages. |

Raises
| Type | Description | 
| ---- | ----------- | 
| ```NoMorePagesException``` | When there are no pages left. |
<details>
<summary>Code example</summary>

```python
>>> print(records_page.has_more)
True
```

</details>

### ```MediahavenPageObject.nr_of_results```
Returns:
| Type | Description | 
| ---- | ----------- | 
| ```int``` | Number of results on current page. |

<details>
<summary>Code example</summary>

```python
>>> print(current_page.nr_of_results)
10
```

</details>

### ```MediahavenPageObject.total_nr_of_results```
Returns:
| Type | Description | 
| ---- | ----------- | 
| ```int``` | Total number of results of query. |

<details>
<summary>Code example</summary>

```python
>>> print(current_page.total_nr_of_results)
10
```

</details>

### ```MediahavenPageObject.start_index```
Returns:
| Type | Description | 
| ---- | ----------- | 
| ```int``` | Current page's start index. |

<details>
<summary>Code example</summary>

```python
>>> print(current_page.start_index)
10
```

</details>

### ```MediahavenPageObject.raw_response```
Returns:
| Type | Description | 
| ---- | ----------- | 
| ```str``` | Raw response text. |

<details>
<summary>Code example</summary>

```python
>>> print(current_page.raw_response)
{...}
```

</details>