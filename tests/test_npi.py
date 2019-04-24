from npyi.npi import NPI
from npyi import exceptions
import pytest

npi = NPI()


def test_invalid_version():
    with pytest.raises(exceptions.InvalidVersionException):
        npi.search(version='1.5', search_params={'first_name': 'James'})


def test_deprecated_version():
    with pytest.deprecated_call():
        npi.search(version='1.0', search_params={'first_name': 'James'})
    with pytest.deprecated_call():
        npi.search(version='2.0', search_params={'first_name': 'James'})


def test_use_first_name_alias_valid_values():
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': True})
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "True"})
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "true"})
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': False})
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "False"})
    npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "false"})
    with pytest.raises(exceptions.InvalidUseFirstNameAliasException):
        npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "yes"})
        npi.search(search_params={'first_name': 'James', 'use_first_name_alias': "no"})


def test_invalid_search_param():
    with pytest.raises(exceptions.InvalidParamException):
        npi.search(search_params={'first_name': 'James', 'invalid': 'param'})


def test_search_invalid_response():
    with pytest.raises(exceptions.NPyIException):
        npi.search(search_params={'state': 'CA'})
    with pytest.raises(exceptions.NPyIException):
        npi.search(search_params={'use_first_name_alias': True})


def test_valid_search_params():
    npi_result = npi.search(search_params={'number': '1417367343'})
    assert len(npi_result['results']) == 1
    state_result = npi.search(search_params={'first_name': 'James', 'state': 'CA'})
    assert all([
        l['state'] == 'CA'
        for r in state_result['results']
        for l in r['addresses']
    ])


def test_limit():
    results = npi.search({'first_name': 'Jeffrey'}, limit=123)
    assert results['result_count'] == 123
    results = npi.search({'first_name': 'Jeffrey'})
    assert results['result_count'] == 10


def test_skip():
    no_skip = npi.search({'first_name': 'Jeffrey'}, limit=1)
    skip = npi.search({'first_name': 'Jeffrey'}, limit=1, skip=1)
    assert no_skip['results'] != skip['results']
    redo_search_no_skip = npi.search({'first_name': 'Jeffrey'}, limit=1)
    assert no_skip['results'] == redo_search_no_skip['results']
