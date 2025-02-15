import requests
import json

url = 'https://6rlj4ydnkovjlz2b5w75pgpnwu0chhfp.lambda-url.us-east-1.on.aws/'

payload = {
			"submitterEmail": "fridkis2@illinois.edu", # your email as it appears on the MP instruction page
			"secret": "1PTaoPVeM6gWLYrM", # your secret key as it appears on the MP instruction page
			"dbApi": "https://zhwfwtqyrb.execute-api.us-east-1.amazonaws.com/mp6-stage1" # Your API Gateway POST API invoke url
		}

print(json.dumps(payload))
print("Running the autograder. This might take several seconds...")
r = requests.post(url, data=json.dumps(payload), headers = {"Content-Type": "application/json"})


print(r)
print(r.status_code, r.reason)
print(r.text)