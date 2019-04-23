from npyi.npi import NPI
from npyi import exceptions
import pytest


def test_search_first_name():
    npi = NPI()
    npi.search({'first_name': 'James'})


def test_invalid_param():
    npi = NPI()
    with pytest.raises(exceptions.InvalidParamException):
        npi.search({'invalid': 'param'})

def test_invalid_version():
    npi = NPI()
    with pytest.raises(exceptions.InvalidVersionException):
        npi.search(version='1.5', search_params={'first_name': 'James'})

# def test_invalid_additional_search_param():
#     npi = NPI()
#     results = npi.search({'test': 'CA'})
#     print(results)
#     raise

