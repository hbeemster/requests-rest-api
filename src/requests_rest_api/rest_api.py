"""REST API module.


API:
    https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.1
"""
import json
import logging
from contextlib import suppress

from requests import Session
from typing import Dict, Union, Optional

import requests

from requests_rest_api.constants import GET, HEAD, POST, PUT, DELETE, PATCH, STATUS_CODES
from requests_rest_api-rest-api.errors import RequestError

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------
def get_request(
    url: str,
    *,
    params: Optional[Dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[Dict, None]:
    """"""
    if status_codes is None:
        status_codes = [200]
    return _request(
        method="GET",
        url=url,
        params=params,
        status_codes=status_codes,
        session=session,
        **kwargs,
    )


# ------------------------------------------------------------------------
def post_request(
    url: str,
    *,
    data: Optional[dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[Dict, None]:
    """"""
    if status_codes is None:
        status_codes = [200, 201, 204]

    return _request(
        method="POST",
        url=url,
        data=data,
        status_codes=status_codes,
        session=session,
        **kwargs,
    )


# ------------------------------------------------------------------------
def put_request(
    url: str,
    *,
    data: Optional[dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[Dict, None]:
    """"""
    if status_codes is None:
        status_codes = [200, 202, 204]

    return _request(
        method="PUT",
        url=url,
        data=data,
        status_codes=status_codes,
        session=session,
        **kwargs,
    )

# ------------------------------------------------------------------------
def patch_request(
    url: str,
    *,
    data: Optional[dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[Dict, None]:
    """"""
    if status_codes is None:
        status_codes = [200, 204]

    return _request(
        method="PATCH",
        url=url,
        data=data,
        status_codes=status_codes,
        session=session,
        **kwargs,
    )

# ------------------------------------------------------------------------
def delete_request(
    url: str,
    *,
        status_codes: Optional[list] = None,
        session: Optional[Session] = None,
        **kwargs,
) -> Union[bool, None]:
    if status_codes is None:
        status_codes = [200, 202, 204]

    return _request(
        method="DELETE",
        url=url,
        status_codes=status_codes,
        session=session,
        **kwargs,
    )



# ------------------------------------------------------------------------
# protected functions
# ------------------------------------------------------------------------
def _request(
    *,
    method: str,
    url: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[bool, str, dict]:
    """submits http request"""

    http_method = method.upper()

    cleanup_session = False
    if session is None:
        session = Session()
        cleanup_session = True

    try:
        if GET == http_method:
            response = session.get(url, params=params, **kwargs)
        elif HEAD == http_method:
            response = session.head(url, **kwargs)
        elif POST == http_method:
            response = session.post(url, data=data, **kwargs)
        elif PUT == http_method:
            response = session.put(url, data=data, **kwargs)
        elif DELETE == http_method:
            response = session.delete(url, **kwargs)
        elif PATCH == http_method:
            response = session.patch(url, data=data, **kwargs)
        else:
            raise RequestError(f"HTTP method type '{http_method}' is not supported.")

        # raise exception for error codes 4xx or 5xx
        response.raise_for_status()
    except (
        requests.exceptions.HTTPError,
        requests.ConnectionError,
        requests.Timeout,
        requests.exceptions.RequestException,
    ) as exception:
        raise RequestError(exception, response.status_code)
    finally:
        if cleanup_session:
            session.close()

    # get list of expected status codes, otherwise override with provided codes
    expected_status_codes = _expected_status_code(http_method) if status_codes is None else status_codes

    # check if status code returned is "expected", otherwise raise ``HTTPError``
    if response.status_code not in expected_status_codes:
        raise RequestError(
            f"Unexpected HTTP status code '{response.status_code}' returned with " f"reason '{response.reason}'"
        )

    # for responses with no content, return True to indicate
    # that the request was successful
    if not response.content:
        return True

    with suppress(json.JSONDecodeError):
        return response.json()

    return response.text


def _expected_status_code(http_method: str) -> list:
    """sets expected status codes based on method type"""
    status_codes = [200]
    with suppress(KeyError):
        status_codes = STATUS_CODES[http_method]
    return status_codes
