namespace = 'free-service'
with open("free-service-job.yaml", 'r') as f:
	try:
		job_manifest = yaml.safe_load(f)
		api_response = batch_v1.create_namespaced_job(body=job_manifest, namespace=namespace)
		print(f"Job created in namespace '{namespace}'. Status: {api_response.status}")
	except client.rest.ApiException as e:
		print(f"Exception when creating Job: {e}\n")
	except FileNotFoundError:
		print(f"Error: YAML file not found: {yaml_file}")
        
        
namespace = 'default'
with open("premium-service-job.yaml", 'r') as f:
    try:
        job_manifest = yaml.safe_load(f)
        api_response = batch_v1.create_namespaced_job(body=job_manifest, namespace=namespace)
        print(f"Job created in namespace '{namespace}'. Status: {api_response.status}")
    except client.rest.ApiException as e:
        print(f"Exception when creating Job: {e}\n")
    except FileNotFoundError:
        print(f"Error: YAML file not found: {yaml_file}")