"""Exception classes raised by various operations within pyguts."""


class InvalidMessageError(Exception):
    """Raised when a message creation, registration or addition is rejected."""


class UnknownMessageError(Exception):
    """Raised when an unregistered message id is encountered."""
