# Bible is here https://github.com/metabase/metabase/wiki/Using-the-REST-API
import requests
from requests.auth import HTTPBasicAuth
import json

# POST request for session token
user = placeholder
password = placeholder2
URL = "https://metabase.ec2.kindredai.net/api/session"
auth = HTTPBasicAuth(user, password)

headers = {
    "Content-Type": "application/json"

}

authorization = '{"username": "cliff.weir@kindred.ai", "password": "Boromokott2390!"}'

r = requests.post(headers=headers, data=authorization, url=URL)
print(r.text) # prints that my password is not linked to my account.

# GET request will go here, using a token generated by the POST request. As of right now metabase doesn't have a
# password linked to my account so this has a pin put in it until after my code review.

