from crossengage.client import CrossengageClient

client = CrossengageClient(client_token='INSERT_YOUR_TOKEN_HERE')

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

# 2. Bulk create - update
user1 = {
    'id': '2',
    'email': 'test@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
    'silos': ['1', '2', '3']
}
user2 = {
    'id': '3',
    'email': 'test2@example.com',
    'firstName': 'First name2',
    'lastName': 'Last name2',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
    'silos': ['1', '2', '3']
}
users = [user1, user2]
response = client.update_users_bulk(users=users)
for data in response['updated']:
    if data['success']:
        print 'BULK #' + data['id'] + ' success'
    else:
        print 'BULK #' + data['id'] + ' FAIL'
        print data['errors']

# 3. Delete user
response = client.delete_user(user={'id': '1'})
if response['status_code'] == 204:
    print '#1 Deleted successful!'
else:
    print 'Something went wrong via DELETE request'

# 4. Trying to update with invalid field, API should return error
response = client.update_user(user={
    'id': '1',
    'email': 'test1@example.com',
    'firstName': 'First name',
    'lastName': 'Last name',
    'birthday': '1982-08-30',
    'createdAt': '2015-10-02T08:23:53Z',
    'gender': 'male',
    'INVALID FIELD': 'male',
})

if response['success']:
    print '# 1 Updated with invalid fields successful!'
else:
    print response['errors']

# 5. Add new user attributes
response = client.add_user_attribute('silos', client.ATTRIBUTE_ARRAY, client.ATTRIBUTE_STRING)

if response['success']:
    print 'Added user attribute `silos` successful!'
else:
    print response['errors']

# 6. List user attributes
response = client.list_user_attributes(offset=37, limit=10)
if response['status_code'] == 200:
    print 'Got list user attributes successful!'
    print response['attributes']
else:
    print response['errors']
