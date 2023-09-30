# Rest API Manager

[![PyPI - Version](https://img.shields.io/pypi/v/requests-rest-api.svg)](https://pypi.org/project/requests-rest-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests-rest-api.svg)](https://pypi.org/project/requests-rest-api)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Introduction
The `requests-rest-api` package is a thin wrapper around the [requests](https://requests.readthedocs.io) library with functions to make REST API calls.

## Examples

### Simple GET:

```python
from requests_rest_api.rest_api import get_request

get_request("https://reqres.in/api/users/2")
```


---
**NOTE**

All the functions simply pass all parameters to the `requests` equivalent, so if you can always add more parameters if needed.
For example add the `headers` parameter like this:

```python
from requests_rest_api.rest_api import get_request

get_request("https://reqres.in/api/users/2", headers={"Token": "123"})
```

---

### Example with a Session
`requests` has a [Session](https://requests.readthedocs.io/en/latest/api/#request-sessions) class that can take care of connection-pooling, authorisation, headers, cookies etc.

This example would set a token for the session:
```python
from requests import Session
from requests_rest_api.rest_api import get_request

with Session(headers={"Token": "123"}) as session:
    result = get_request("https://reqres.in/api/users/2", session=session)
```



## Installation

```console
pip install requests-rest-api
```

## License

`requests-rest-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
