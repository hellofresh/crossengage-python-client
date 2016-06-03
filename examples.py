from crossengage.client import CrossengageClient

client = CrossengageClient(client_token='INSERT_YOUR_TOKEN_HERE')

# 1. Create / update new user and send
r = client.update_user(payload={
    'id': '1',
    'email': 'test@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
})

if r['success']:
    print 'Successful!'
else:
    print r['client_error']
    print r['errors']

# 2. Delete user
r = client.delete_user(payload={'id': '1'})
if r['success']:
    print '2 Deleted successful!'
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
    print '3 Updated successful!'
else:
    print r['client_error']
    print r['errors']

# 4. Add new user attributes
r = client.add_user_attribute(
    attribute_name='our_new_attribute',
    attribute_type=client.ATTRIBUTE_ARRAY,
    nested_type=client.ATTRIBUTE_STRING
)

if r['success']:
    print '4 Added user attribute successful!'
else:
    print r['client_error']
    print r['errors']

# 5. List user attributes
r = client.list_user_attributes(offset=0, limit=10)
if r['success']:
    print '5 Got list user attributes successful!'
    print r['attributes']
else:
    print r['client_error']
    print r['errors']
