# MediaHaven Python Library

## Synopsis

The Mediahaven Python library provides a way to communicate with MediaHaven via the v2 REST API.

## Documentation

For more information about the internals of this library: see the automatically generated [documentation](/docs/README.md).

## Usage

```python
>>> import os
>>> 
>>> from mediahaven import MediaHaven
>>> from mediahaven.oauth2 import ROPCGrant, RequestTokenError
>>> 
>>> # Get the credentials from env vars.
>>> client_id = os.environ["CLIENT_ID"]
>>> client_secret = os.environ["CLIENT_SECRET"]
>>> username = os.environ["USERNAME"]
>>> password = os.environ["PASSWORD"]
>>> url = os.environ["MH_URL"]
>>> 
>>> # Create a ROPC grant
>>> grant = ROPCGrant(url, client_id, client_secret)
>>> # Request a token
>>> try:
...     grant.request_token(username, password)
... except RequestTokenError as e:
...     print(e)
... 
>>> # Initialize the MH client
>>> client = MediaHaven(url, grant)

>>> # Get record based on record ID
>>> record = client.records.get("570...33b")
>>> print(record.Internal.ArchiveStatus)
on_disk
>>> print(record.Dynamic.PID)
qs...8q

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

>>> # Get next page
>>> print(records_page.has_more)
True
>>> next_page = records_page.next_page()
>>> print(next_page.nr_of_results)
10
>>> print(next_page.total_nr_of_results)
22
>>> print(next_page.start_index)
10
>>> print(next_page[0].Dynamic.PID)
2z...40

>>> # Work via generator
>>> for record in records_page.as_generator():
...     print(record.Dynamic.PID)
... 
w3...0k
<SNIP 20 IDs>
9s...5t
```