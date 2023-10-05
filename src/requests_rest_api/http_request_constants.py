from enum import Enum
from http import HTTPStatus
from typing import Optional


# supported request methods
class HTTPVerb(str, Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


# expected http status codes per HTTP Verb
STATUS_CODES_PER_HTTP_VERB = {
    HTTPVerb.GET: [HTTPStatus.OK],
    HTTPVerb.HEAD: [HTTPStatus.OK],
    HTTPVerb.POST: [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT],
    HTTPVerb.PUT: [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT],
    HTTPVerb.DELETE: [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT],
    HTTPVerb.PATCH: [HTTPStatus.OK, HTTPStatus.NO_CONTENT],
}


def expected_status_codes(
    http_verb: HTTPVerb,
    status_codes: Optional[list] = None,
):
    return STATUS_CODES_PER_HTTP_VERB[http_verb] if status_codes is None else status_codes
