<p align="center">
  <a href="https://hellofresh.com">
    <img width="120" src="https://www.hellofresh.de/images/hellofresh/press/HelloFresh_Logo.png">
  </a>
</p>

# crossengage-python-client
[![Build Status](https://travis-ci.org/hellofresh/crossengage-python-client.svg?branch=master)](https://travis-ci.org/hellofresh/crossengage-python-client)
[![codecov](https://codecov.io/gh/hellofresh/crossengage-python-client/branch/master/graph/badge.svg)](https://codecov.io/gh/hellofresh/crossengage-python-client)

Python client for [Crossengage's API](https://docs.crossengage.io)

Library supports next methods:

**User profile management**
 - `update_user(self, user)`
 - `delete_user(self, user)`
 - `delete_user_by_xng_id(self, user)`

**User attributes management**
- `add_user_attribute(self, attribute_name, attribute_type, nested_type)`
- `add_nested_user_attribute(self, parent_name, attribute_name, attribute_type)`
- `list_user_attributes(self, offset, limit)`
- `delete_user_attribute(self, attribute_id)`

**Bulk user management**
- `batch_process(self, delete_list=[], update_list=[])`

**Events management**
- `send_events(self, events, email=None, user_id=None, business_unit=None)`

### Owner
[Alexander Zhilyaev](mailto:azh@hellofresh.com)

### How to install

Make sure you have Python 2.7.11+ installed and run:

```
$ git clone git@github.com:hellofresh/crossengage-python-client.git
$ cd crossengage-python-client
$ python setup.py install
```

### How to use

```python
from crossengage.client import CrossengageClient

client = CrossengageClient(client_token='YOUR_TOKEN')

# 1. Create / update new user and send
response = client.update_user(user={
    'id': '2',
    'email': 'test@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
})

if response['success']:
    print 'Create / Update Successful!'
else:
    print response['errors']

```
For more examples, check `examples.py`.

### How to test

To run the unit tests, make sure you have the [nose](http://nose.readthedocs.org/) module instaled and run the following from the repository root directory:

`$ make build && make test`
