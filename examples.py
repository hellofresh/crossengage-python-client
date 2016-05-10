from crossengage.client import CrossengageClient

client = CrossengageClient(client_token='INSERT_YOUR_TOKEN_HERE')

# 1. Create new user and send
r = client.create_user(payload={
    'id': '1',
    'email': 'test@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
})

if r['success']:
    print 'Created successful!'
else:
    print r['client_error']
    print r['errors']

# 2. Change some data of our user and send
r = client.update_user(payload={
    'id': '1',
    'email': 'test1@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
})

if r['success']:
    print 'Updated successful!'
else:
    print r['client_error']
    print r['errors']

# 3. Delete user
r = client.delete_user(payload={'id': '1'})
if r['success']:
    print 'Deleted successful!'
else:
    print r['client_error']
    print r['errors']

# 3. Trying to update with invalid field, API should return error
r = client.update_user(payload={
    'id': '1',
    'email': 'test1@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
    'INVALID FIELD': 'male',
})

if r['success']:
    print 'Updated successful!'
else:
    print r['client_error']
    print r['errors']
