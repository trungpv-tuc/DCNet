import requests
from requests.auth import HTTPBasicAuth
import json
import sys

with open('flowmirror.json') as json_file:
     json_rule = json.load(json_file)
print json_rule

headers = {'Content-Type':'application/json' , 'Accept':'application/json'}
response = requests.post('http://127.0.0.1:8181/onos/v1/flowobjectives/of%3A0000041401500001/forward?appId=org.onosproject.fwd', data=json_rule, auth=('onos', 'rocks'), headers=headers)
print response.status_code

