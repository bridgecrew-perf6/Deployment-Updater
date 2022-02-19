from kubernetes import client, config

config.load_incluster_config()
core = client.CoreV1Api()
apps = client.AppsV1Api()

def get_pods():
    return core.list_pod_for_all_namespaces(watch=False)


def get_deployments():
    return apps.list_deployment_for_all_namespaces(watch=False)


def update_deployment_container_tag(namespace, deployment, tag):
    return apps.list_namespaced_deployment(namespace)
