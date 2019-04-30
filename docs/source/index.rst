Welcome to the NPyI documentation!
=====================================
NPyI is an API wrapper around the `NPPES API <https://npiregistry.cms.hhs.gov/registry/help-api/>`_.

Here's some sample usage::

    from npyi import npi

    # sample search by first_name / last_name
    response = npi.search(search_params={'first_name': 'Andrew', 'last_name': 'Jackson'})
    print(response.keys()) # dict_keys(['result_count', 'results'])
    first_entry = response['results'][0]
    print(first_entry['basic']['first_name']) # ANDREW
    print(first_entry['basic']['last_name']) # JACKSON

    # sample search by NPI number
    response = search(search_params={'number': '1417367343'})
    print(response['result_count']) # 1
    print(response['results'][0]['number']) # 1417367343

    # sample search by city
    response = search(search_params={'city': 'San Francisco'})
    first_entry = response['results'][0]
    print(len(first_entry['addresses'])) # 2 (different address purposes - LOCATION and MAILING)
    print(first_entry['addresses'][0]['city']) # SAN FRANCISCO

    # limit example
    response = search(search_params={'first_name': 'Andrew', 'city': 'New York'}, limit=50)
    print(response['result_count']) # 50
    response = search(search_params={'first_name': 'Andrew', 'city': 'New York'}, limit=1000)
    print(response['result_count']) # 200 (200 is the max)
    response = search(search_params={'first_name': 'Andrew', 'city': 'New York'})
    print(response['result_count']) # 10 (10 is the default)


API Documentation
-----------------
All the API documentation.

.. toctree::
   :maxdepth: 1

   npi
   exceptions
