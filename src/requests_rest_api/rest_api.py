"""Requests REST API module."""
import json
import logging
from typing import Dict, Optional, Union

import requests
from requests import Session

from requests_rest_api.errors import RequestError
from requests_rest_api.http_request_constants import HTTPVerb, expected_status_codes

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
    return _request(
        http_verb=HTTPVerb.GET,
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
    return _request(
        http_verb=HTTPVerb.POST,
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
    return _request(
        http_verb=HTTPVerb.PUT,
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
    return _request(
        http_verb=HTTPVerb.PATCH,
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
    return _request(
        http_verb=HTTPVerb.DELETE,
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
    http_verb: HTTPVerb,
    url: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    status_codes: Optional[list] = None,
    session: Optional[Session] = None,
    **kwargs,
) -> Union[bool, str, dict]:
    """submits http request"""

    if session:
        response = _send_request(http_verb=http_verb, url=url, session=session, params=params, data=data, **kwargs)
    else:
        with Session() as session:
            response = _send_request(http_verb=http_verb, url=url, session=session, params=params, data=data, **kwargs)

    # check if status code returned is "expected", otherwise raise ``HTTPError``
    if response.status_code not in expected_status_codes(
        http_verb, status_codes
    ):
        raise RequestError(
            f"Unexpected HTTP status code '{response.status_code}' returned with reason '{response.reason}'"
        )

    # for responses with no content, return True to indicate
    # that the request was successful
    if not response.content:
        return True

    # Test if we did get a JSON response
    if 'application/json' not in response.headers.get('Content-Type', ''):
        raise RequestError(
            f"The response was not valid JSON: '{response.text}'"
        )

    try:
        return response.json()
    except json.JSONDecodeError as e:
        raise RequestError(
            f"The response was not valid JSON: '{response.text}', error '{e}'"
        ) from e


# ------------------------------------------------------------------------
def _send_request(
    *,
    http_verb: HTTPVerb,
    url: str,
    session: Session,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    **kwargs,
):
    """"""
    response = None
    try:
        if http_verb == HTTPVerb.GET:
            response = session.get(url, params=params, **kwargs)
        elif http_verb == HTTPVerb.HEAD:
            response = session.head(url, **kwargs)
        elif http_verb == HTTPVerb.POST:
            response = session.post(url, data=data, **kwargs)
        elif http_verb == HTTPVerb.PUT:
            response = session.put(url, data=data, **kwargs)
        elif http_verb == HTTPVerb.DELETE:
            response = session.delete(url, **kwargs)
        elif http_verb == HTTPVerb.PATCH:
            response = session.patch(url, data=data, **kwargs)
        # raise exception for error codes 4xx or 5xx
        response.raise_for_status()
    except (
        requests.exceptions.HTTPError,
        requests.ConnectionError,
        requests.Timeout,
        requests.exceptions.RequestException,
    ) as e:
        msg = f"Failed to execute the '{http_verb}' request."
        if response:
            msg = f"{msg} - status_code: {response.status_code}"
        msg = f"{msg} - error: {e}"
        raise RequestError(msg) from e

    return response
