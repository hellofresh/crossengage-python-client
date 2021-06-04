<p align="center">
  <a href="https://hellofresh.com">
    <img width="120" src="https://www.hellofresh.de/images/hellofresh/press/HelloFresh_Logo.png">
  </a>
</p>

# crossengage-python-client
[![Build Status](https://travis-ci.org/hellofresh/crossengage-python-client.svg?branch=master)](https://travis-ci.org/hellofresh/crossengage-python-client)

 🚨Info 🚨:  Project is deprecated and archived. Please fork archived repository to continue development on your own. 

Python client for [Crossengage's API](https://docs.crossengage.io)

Library supports next methods:

**User profile management**
 - `get_user(self, user)` | v2
 - `update_user(self, user)` | v1
 - `update_user_async(self, user)` | v2
 - `delete_user(self, user)` | v1
 - `delete_user_async(self, user)` | v2
 - `delete_user_by_xng_id(self, user)` | v1
 - `track_user_task(self, tracking_id)` | v2

**User attributes management**
- `add_user_attribute(self, attribute_name, attribute_type, nested_type)` | v1
- `add_nested_user_attribute(self, parent_name, attribute_name, attribute_type)` | v1
- `list_user_attributes(self, offset, limit)` | v1
- `delete_user_attribute(self, attribute_id)` | v1

**Bulk user management**
- `batch_process(self, delete_list=[], update_list=[])` | v1
- `batch_process_async(self, delete_list=[], update_list=[])` | v2

**Events management**
- `send_events(self, events, email=None, user_id=None, business_unit=None)` | v1

**Opt-Out Management**
 - `get_user_opt_out_status(self, user_id)` | v1
 - `update_user_opt_out_status(self, user_id, channel_name)` | v1
 - `update_user_opt_in_status(self, user_id, channel_name)` | v1

### Owner
[Alexander Zhilyaev](mailto:azh@hellofresh.com)

### How to install

Make sure you have Python 2.7.11+ or Python 3.4+ installed and run:

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
    print('Create / Update Successful!')
else:
    print(response['errors'])

```
For more examples, check `examples.py`.

### How to test

To run the unit tests, make sure you have the [nose](http://nose.readthedocs.org/) module instaled and run the following from the repository root directory:

`$ make setup && make test`
