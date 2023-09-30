from enum import Enum
from typing import Optional


# supported request methods
class RequestMethod(str, Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


# expected http status codes per method type
STATUS_CODES_PER_REQUEST_METHOD = {
    RequestMethod.GET: [200],
    RequestMethod.HEAD: [200],
    RequestMethod.POST: [200, 201, 204],
    RequestMethod.PUT: [200, 202, 204],
    RequestMethod.DELETE: [200, 202, 204],
    RequestMethod.PATCH: [200, 204],
}


def expected_status_codes(
    method: RequestMethod,
    status_codes: Optional[list] = None,
):
    return STATUS_CODES_PER_REQUEST_METHOD[method] if status_codes is None else status_codes
