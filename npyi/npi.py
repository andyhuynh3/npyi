import json
import warnings

import requests
from .exceptions import (
    InvalidSearchParamException,
    InvalidVersionException,
    InvalidUseFirstNameAliasException,
    InvalidAddressPurposeException,
    NPyIException
)


BASE_URI = 'https://npiregistry.cms.hhs.gov/api/'
VALID_SEARCH_PARAMS = (
    'number',
    'enumeration_type',
    'taxonomy_description',
    'first_name',
    'use_first_name_alias',
    'last_name',
    'organization_name',
    'address_purpose',
    'city',
    'state',
    'postal_code',
    'country_code',
)
VALID_VERSIONS = ('1.0', '2.0', '2.1',)
VALID_ADDRESS_PURPOSE_VALUES = (
    'LOCATION', 'MAILING', 'PRIMARY', 'SECONDARY',
)


def search(
    search_params,
    version='2.1',
    limit=None,
    skip=None
):
    """
    Main wrapper function around the NPPES API.

    :param search_params: Search criteria to the NPPES API. See VALID_SEARCH_PARAMS
        for list of valid search params and
        https://npiregistry.cms.hhs.gov/registry/help-api for parameter descriptions.
    :type search_params: dict
    :param version: NPPES API version to use, defaults to '2.1'.
    :type version: str/int, optional
    :param limit: Limit results returned from API, defaults to None. If no value is
        passed, 10 results are returned by default.
    :type limit: int, optional
    :param skip: Bypass first N results from the response, defaults to None.
    :type skip: int, optional
    :return: API response as a dictionary, containing a "results_count"
        and "results" key.
    :rtype: dict
    """

    version = _clean_version(version)
    _validate_version(version)

    _validate_search_params(search_params)

    if 'use_first_name_alias' in search_params:
        use_first_name_alias = search_params['use_first_name_alias']
        use_first_name_alias = _clean_use_first_name_alias(
            use_first_name_alias
        )
        _validate_use_first_name_alias(use_first_name_alias)
        search_params['use_first_name_alias'] = use_first_name_alias

    if 'address_purpose' in search_params:
        address_purpose = search_params['address_purpose']
        address_purpose = _clear_address_purpose(
            address_purpose
        )
        _validate_address_purpose(address_purpose)
        search_params['address_purpose'] = address_purpose

    search_params['version'] = version

    if limit is not None:
        search_params['limit'] = limit
    if skip is not None:
        search_params['skip'] = skip

    response = requests.get(BASE_URI, params=search_params).json()
    _validate_response(response)

    return response


def _clean_version(version):
    """
    Convert version to string and append decimal if appropriate and missing

    :param version: NPPES API version
    :type version: int/str
    :return: The cleaned version
    :rtype: str
    """
    version = str(version)
    if version in ('1', '2'):
        version += '.0'
    return version


def _validate_version(version):
    """
    Validate version is an valid value

    :param version: NPPES API version
    :type version: str
    :raises InvalidVersionException: if API version is invalid
    """
    if version not in VALID_VERSIONS:
        valid_version_str = ', '.join(VALID_VERSIONS)
        raise InvalidVersionException(
            '{} is not a supported version. Supported versions are: {}'.format(
                version, valid_version_str
            )
        )
    if version == '1.0':
        warnings.warn(
            'Version 1.0 of the NPPES API will be deprecated on 2019-06-01',
            DeprecationWarning
        )
    if version == '2.0':
        warnings.warn(
            'Version 2.0 of the NPPES API will be deprecated on 2019-09-01',
            DeprecationWarning
        )


def _clean_use_first_name_alias(use_first_name_alias):
    """
    Converts "True"/"true"/"False"/"false" from a string to a bool

    :param use_first_name_alias: The use_first_name_alias API param value
    :type use_first_name_alias: bool/str
    :return: The cleaned use_first_name_alias value
    :rtype: bool/str
    """
    if (
        isinstance(use_first_name_alias, str) and
        use_first_name_alias.lower() in ("true", "false")
    ):
        return json.loads(use_first_name_alias.lower())
    else:
        return use_first_name_alias


def _validate_use_first_name_alias(use_first_name_alias):
    """
    Validates use_first_name_alias is a valid value

    :param use_first_name_alias: The use_first_name_alias API param value
    :type use_first_name_alias: bool
    :raises InvalidUseFirstNameAliasException: if use_first_name_alias is not bool
    """
    if not isinstance(use_first_name_alias, bool):
        raise InvalidUseFirstNameAliasException(
            '{} is not a valid value for the use_first_name_alias param. '
            'use_first_name_alias must be a bool'.format(
                use_first_name_alias,
            )
        )


def _clear_address_purpose(address_purpose):
    """
    Converts address_purpose to all uppercase

    :param address_purpose: The address_purpose API param value
    :type address_purpose: str
    :return: Cleaned address_purpose value
    :rtype: str
    """
    return address_purpose.upper()


def _validate_address_purpose(address_purpose):
    """
    Validtes address_purpose is a valid value

    :param address_purpose: The address_purpose API param value
    :type address_purpose: str
    :raises InvalidAddressPurposeException: if address_purpose is not a valid value
    """
    if address_purpose not in VALID_ADDRESS_PURPOSE_VALUES:
        valid_address_purpose_str = ', '.join(
            VALID_ADDRESS_PURPOSE_VALUES
        )
        raise InvalidAddressPurposeException(
            '{} is not a valid value for the address_purpose param. '
            'Valid values are: {}'.format(
                address_purpose,
                valid_address_purpose_str
            )
        )


def _validate_search_params(search_params):
    """
    Validates that the keys in search_params are valid values.

    :param search_params: Mapping of API param to value
    :type search_params: dict
    :raises InvalidSearchParamException: if any keys are invalid values
    """
    for param in search_params:
        if param not in VALID_SEARCH_PARAMS:
            valid_search_params_str = ', '.join(VALID_SEARCH_PARAMS)
            raise InvalidSearchParamException(
                "{} is not a valid parameter. Valid search_params are: {}".format(
                    param,
                    valid_search_params_str
                )
            )


def _validate_response(response):
    """
    Validates API response to ensure ther are no errors.

    :param response: The API response
    :type response: dict
    :raises NPyIException: if the response returns an error
    """
    if 'Errors' in response:
        first_error = response['Errors'][0]['description']
        raise NPyIException(first_error)
