from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()
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
    namespace = 'free-service'
    with open("free-service-job.yaml", 'r') as f:
        try:
            job_manifest = yaml.safe_load(f)
            api_response = batch_v1.create_namespaced_job(body=job_manifest, namespace=namespace)
            print(f"Job created in namespace '{namespace}'. Status: {api_response.status}")
            return "success"
        except client.rest.ApiException as e:
            print(f"Exception when creating Job: {e}\n")
            return f"Exception when creating Job: {e}\n"
        except FileNotFoundError:
            print(f"Error: YAML file not found: {yaml_file}")
            return f"Error: YAML file not found: {yaml_file}"

@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    namespace = 'default'
    with open("premium-service-job.yaml", 'r') as f:
        try:
            job_manifest = yaml.safe_load(f)
            api_response = batch_v1.create_namespaced_job(body=job_manifest, namespace=namespace)
            print(f"Job created in namespace '{namespace}'. Status: {api_response.status}")
            return "success"
        except client.rest.ApiException as e:
            print(f"Exception when creating Job: {e}\n")
            return f"Exception when creating Job: {e}\n"
        except FileNotFoundError:
            print(f"Error: YAML file not found: {yaml_file}")
            return f"Error: YAML file not found: {yaml_file}"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
    
# References
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-linux.html
# https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CoreV1Api.md#list_pod_for_all_namespaces
# https://stackoverflow.com/questions/66683268/how-can-i-list-all-pods-in-a-kubernetes-cluster-in-python
# https://www.google.com/search?q=how+to+run+kubernetes+job+from+yaml+file+via+python&sca_esv=51ee083cf20858f1&rlz=1C1CHBF_enUS1071US1071&ei=t339Z87mIO6awbkPyLLS0Ao&ved=0ahUKEwiOnqe8u9iMAxVuTTABHUiZFKoQ4dUDCBA&uact=5&oq=how+to+run+kubernetes+job+from+yaml+file+via+python&gs_lp=Egxnd3Mtd2l6LXNlcnAiM2hvdyB0byBydW4ga3ViZXJuZXRlcyBqb2IgZnJvbSB5YW1sIGZpbGUgdmlhIHB5dGhvbjIFEAAY7wUyCBAAGKIEGIkFMggQABiABBiiBDIFEAAY7wUyCBAAGKIEGIkFSL8eUK4KWO8ccAF4AJABAJgB7gGgAbgUqgEGMC4xMy4zuAEDyAEA-AEBmAIFoAL-BMICChAAGLADGNYEGEfCAggQIRigARjDBMICChAhGKABGMMEGAqYAwCIBgGQBgiSBwUxLjMuMaAH0DqyBwUwLjMuMbgH9QQ&sclient=gws-wiz-serp