class MarshMallowJsonError(Exception):
    """
    Encapsulates our exceptions.
    """


class ValidationError(MarshMallowJsonError):
    """
    A definition is not well defined.
    """
