from kubernetes import client, config

config.load_incluster_config()
v1 = client.CoreV1Api()

def get_pods():
    return v1.list_pod_for_all_namespaces(watch=False)
