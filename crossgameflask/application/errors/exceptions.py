class AttributeIsNotFoundInTheFormException(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)


class IncorrectStringValue(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)


class NoUserInTheSession(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)
