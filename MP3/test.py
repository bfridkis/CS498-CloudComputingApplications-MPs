import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-lexv2-autograder"

payload = {
	"graphApi": "https://csjq80nvsk.execute-api.us-east-1.amazonaws.com/MP3",
	"botId": "ORWO4MOZ3J", 
	"botAliasId": "L7X8DJ38OX",
	"identityPoolId": "us-east-1:2a333ccd-7028-41de-af66-104e6947fae3",
	"accountId": "024848464133",
	"submitterEmail": "fridkis2@illinois.edu",
	"secret": "Ac3jIYxOKd3drleI",
	"region": "us-east-1" #<Region where your lex is deployed (Ex: us-east-1)>
    }

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)