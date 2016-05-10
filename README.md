<p align="center">
  <a href="https://hellofresh.com">
    <img width="120" src="https://www.hellofresh.de/images/hellofresh/press/HelloFresh_Logo.png">
  </a>
</p>

# crossengage-python-client
Python client for Crossengage's API

[ ![Codeship build](https://codeship.com/projects/c70724e0-f905-0133-a8ad-268d110da048/status?branch=master)](https://codeship.com/projects/151121)
### Owner
azh@hellofresh.com

### How to install

Make sure you have Python 2.7.11+ installed

1. `git clone git@github.com:hellofresh/crossengage-python-client.git`
2. Run `setup.py`

### How to use

```python
from crossengage.client import CrossengageClient

client = CrossengageClient(client_token='YOUR_TOKEN')

# 1. Create/update user 
response = client.create_user(payload={
    'id': '1',
    'email': 'test@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
})

if response['success']:
    # do your magic
    pass
else:
    # something went wrong
    print response['client_error']  # for client issues (connection timeout and etc)
    print response['errors'] # for issues on API side (validation error and etc)

```
See another examples in `examples.py`

### Tests

To run unit tests (install [nosetests](http://nose.readthedocs.org/) module before) just run the following command in the repository root directory:

`$ nosetests`
