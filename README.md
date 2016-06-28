<p align="center">
  <a href="https://hellofresh.com">
    <img width="120" src="https://www.hellofresh.de/images/hellofresh/press/HelloFresh_Logo.png">
  </a>
</p>

# crossengage-python-client
Python client for Crossengage's API

[ ![Codeship build](https://codeship.com/projects/c70724e0-f905-0133-a8ad-268d110da048/status?branch=master)](https://codeship.com/projects/151121)
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

`$ nosetests`
