import datetime
from typing import List
from kubernetes import client, config
from kubernetes.client.models import V1DeploymentList, V1Deployment

config.load_incluster_config()
core = client.CoreV1Api()
apps = client.AppsV1Api()


def _find_index(items, filter):
    if not isinstance(filter, callable):
        def _filter(item):
            return item == filter
    else:
        _filter = filter
    for i, item in enumerate(items):
        if _filter(item):
            return i
    return None


def get_pods():
    return core.list_pod_for_all_namespaces(watch=False)


def get_deployments():
    return apps.list_deployment_for_all_namespaces(watch=False)

def restart_deployment(namespace, deployment_name):
    deployments: List[V1Deployment] = apps.list_namespaced_deployment(namespace).items
    i = _find_index(deployments, lambda x: x.metadata.name == deployment_name)
    deployment: V1Deployment = deployments[i]
    if deployment is None:
        return False
    deployment.spec.template.metadata.annotations["kubectl.kubernetes.io/restartedAt"] = datetime.datetime.utcnow().isoformat()
    return apps.patch_namespaced_deployment(deployment_name, namespace, body=deployment)
