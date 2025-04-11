from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    pod_snapshot = v1.list_pod_for_all_namespaces(watch=False)
    
for pod in pod_snapshot.items:
    pods.append({
        "name": pod.metadata.name,
        "ip": pod.status.pod_ip,
        "namespace":pod.metadata.namespace,
        "node":pod.spec.node_name,
        "status": pod.status.phase
        }
    )
output = {"pods": pods}
output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here

    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here

    return "success"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    
# References
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_pod_for_all_namespaces
# https://stackoverflow.com/questions/66683268/how-can-i-list-all-pods-in-a-kubernetes-cluster-in-python