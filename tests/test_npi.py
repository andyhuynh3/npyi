from npyi.npi import search
from npyi import exceptions
import pytest


def test_invalid_version():
    with pytest.raises(exceptions.InvalidVersionException):
        search(version='1.5', search_params={'first_name': 'James'})


def test_deprecated_version():
    with pytest.deprecated_call():
        search(version='1.0', search_params={'first_name': 'James'})
    with pytest.deprecated_call():
        search(version='2.0', search_params={'first_name': 'James'})


def test_use_first_name_alias_valid_values():
    for val in (True, "True", "true", False, "False", "false"):
        search(search_params={'first_name': 'James', 'use_first_name_alias': val})
    with pytest.raises(exceptions.InvalidUseFirstNameAliasException):
        search(search_params={'first_name': 'James', 'use_first_name_alias': "yes"})
    with pytest.raises(exceptions.InvalidUseFirstNameAliasException):
        search(search_params={'first_name': 'James', 'use_first_name_alias': "no"})


def test_invalid_search_param():
    with pytest.raises(exceptions.InvalidSearchParamException):
        search(search_params={'first_name': 'James', 'invalid': 'param'})


def test_search_invalid_response():
    with pytest.raises(exceptions.NPyIException):
        search(search_params={'state': 'CA'})
    with pytest.raises(exceptions.NPyIException):
        search(search_params={'use_first_name_alias': True})


def test_valid_search_params():
    npi_result = search(search_params={'number': '1417367343'})
    assert npi_result['result_count'] == 1
    state_result = search(search_params={'first_name': 'James', 'state': 'CA'})
    assert all([
        l['state'] == 'CA'
        for r in state_result['results']
        for l in r['addresses']
    ])


def test_limit():
    results = search({'first_name': 'Jeffrey'}, limit=123)
    assert results['result_count'] == 123
    results = search({'first_name': 'Jeffrey'})
    assert results['result_count'] == 10


def test_skip():
    no_skip = search({'first_name': 'Jeffrey'}, limit=1)
    skip = search({'first_name': 'Jeffrey'}, limit=1, skip=1)
    assert no_skip['results'] != skip['results']
    redo_search_no_skip = search({'first_name': 'Jeffrey'}, limit=1)
    assert no_skip['results'] == redo_search_no_skip['results']
