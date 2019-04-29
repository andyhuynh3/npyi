class NPyIException(Exception):
    """
    Base exception for module
    """
    pass


class InvalidSearchParamException(NPyIException):
    """
    Exception for invalid search parameters
    """
    pass


class InvalidVersionException(NPyIException):
    """
    Exception for invalid NPPES API versions
    """
    pass


class InvalidUseFirstNameAliasException(NPyIException):
    """
    Exception for invalid used_first_name_alias values
    """
    pass


class InvalidAddressPurposeException(NPyIException):
    """
    Exception for invalid address_purpose values
    """
    pass
