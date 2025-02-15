import requests
import json

# Read Request
payload = {
        "USE_CACHE": "True",
        "REQUEST": "read",
        "SQLS": [1,2,3]
    }
#api = "your dbApi"
api = "https://zhwfwtqyrb.execute-api.us-east-1.amazonaws.com/mp6-stage1"
r = requests.post(api, data=json.dumps(payload))
res = ""
res = r.json()['body']

# Write Request
payload = {
        "USE_CACHE": "True",
        "REQUEST": "write",
        "SQLS": [
            {
              "hero": "yes",
              "name": "fireman",
              "power": "fire",
              "color": "red",
              "xp": "1000001"
            },
            {
              "hero": "no",
              "name": "dogman",
              "power": "bark",
              "color": "brown",
              "xp": "1000002"
            }
        ]
    }
#api = "your dbApi"
api = "https://zhwfwtqyrb.execute-api.us-east-1.amazonaws.com/mp6-stage1"
r = requests.post(api, data=json.dumps(payload))
res = ""
res = r.json()['body']
