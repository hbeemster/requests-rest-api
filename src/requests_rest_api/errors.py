class HTTPError(Exception):
    """base exception used for this module"""

    pass


# class ConfigurationError(HTTPError):
#     """ exception raised when method configuration fails """
#     errno = 1
#     errtype = "CONFIG_ERROR"
#     description = "Invalid configuration property (or properties) detected."
#
#     def __init__(self, message: str) -> NoReturn:
#         super().__init__(message)


class RequestError(HTTPError):
    """Error raised for all requests failures."""

    pass
