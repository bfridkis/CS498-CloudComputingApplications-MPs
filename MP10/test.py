import csv
import requests
import json

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp11"

student = {
    "submitterEmail": "fridkis2@illinois.edu",  # <Your coursera account email>
    "secret": "bQm7NxnZgRgI2l0p",  # <Your secret token from coursera>
    "input_lambda_url": "https://ldm52gfyajrusu3ltm2wvnd3ai0pigfh.lambda-url.us-east-1.on.aws/", # <URL for lambda to write to Kinesis stream>
    "output_lambda_url": "https://qvbo5as2ipjduo5jiq7gkg35za0bvzgu.lambda-url.us-east-1.on.aws/" # <URL for lambda to read table output from S3>
}
lambda_url = "https://njrbzfoij6a7iflndghsrq7mae0gbbyg.lambda-url.us-east-1.on.aws/"

def sendToAutograder(payload):
    r = requests.post(url, data=json.dumps(payload))
    r = requests.post(lambda_url, data=json.dumps(payload),
                      headers={"Content-Type": "application/json"})
    print(r.status_code, r.reason)
    print(r.text)

def main():

    payload = {}
    payload['student'] = student
    print(json.dumps(payload))
    sendToAutograder(payload)
    

if __name__ == "__main__":
    main()