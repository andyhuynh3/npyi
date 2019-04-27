import json
import warnings

import requests
from .exceptions import (
    InvalidParamException,
    InvalidVersionException,
    InvalidUseFirstNameAliasException,
    InvalidAddressPurposeException,
    NPyIException
)


class NPI:

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
        self,
        search_params,
        version='2.1',
        limit=None,
        skip=None
    ):

        version = self._clean_version(version)
        self._validate_version(version)

        self._validate_search_params(search_params)

        if 'use_first_name_alias' in search_params:
            use_first_name_alias = search_params['use_first_name_alias']
            use_first_name_alias = self._clean_use_first_name_alias(
                use_first_name_alias
            )
            self._validate_use_first_name_alias(use_first_name_alias)
            search_params['use_first_name_alias'] = use_first_name_alias

        if 'address_purpose' in search_params:
            address_purpose = search_params['address_purpose']
            address_purpose = self._clear_address_purpose(
                address_purpose
            )
            self._validate_address_purpose(address_purpose)
            search_params['address_purpose'] = address_purpose

        search_params['version'] = version

        if limit is not None:
            search_params['limit'] = limit
        if skip is not None:
            search_params['skip'] = skip

        response = requests.get(self.BASE_URI, params=search_params).json()
        self._validate_response(response)

        return response

    def _clean_version(self, version):
        version = str(version)
        if version in ('1', '2'):
            version += '.0'
        return version

    def _validate_version(self, version):
        if version not in self.VALID_VERSIONS:
            valid_version_str = ', '.join(self.VALID_VERSIONS)
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

    def _clean_use_first_name_alias(self, use_first_name_alias):
        if (
            isinstance(use_first_name_alias, str) and
            use_first_name_alias.lower() in ("true", "false")
        ):
            return json.loads(use_first_name_alias.lower())
        else:
            return use_first_name_alias

    def _validate_use_first_name_alias(self, use_first_name_alias):
        if not isinstance(use_first_name_alias, bool):
            raise InvalidUseFirstNameAliasException(
                '{} is not a valid value for the use_first_name_alias param. '
                'use_first_name_alias must be a bool'.format(
                    use_first_name_alias,
                )
            )

    def _clear_address_purpose(self, address_purpose):
        return address_purpose.upper()

    def _validate_address_purpose(self, address_purpose):
        if address_purpose not in self.VALID_ADDRESS_PURPOSE_VALUES:
            valid_address_purpose_str = ', '.join(
                self.VALID_ADDRESS_PURPOSE_VALUES
            )
            raise InvalidAddressPurposeException(
                '{} is not a valid value for the address_purpose param. '
                'Valid values are: {}'.format(
                    address_purpose,
                    valid_address_purpose_str
                )
            )

    def _validate_search_params(self, search_params):
        for param in search_params:
            if param not in self.VALID_SEARCH_PARAMS:
                valid_search_params_str = ', '.join(self.VALID_SEARCH_PARAMS)
                raise InvalidParamException(
                    "{} is not a valid parameter. Valid search_params are: {}".format(
                        param,
                        valid_search_params_str
                    )
                )

    def _validate_response(self, response):
        if 'Errors' in response:
            first_error = response['Errors'][0]['description']
            raise NPyIException(first_error)
