import imp
from updater.config import webhook_config
from . import app
from . import config
from flask import request, abort
try:
    from . import kube
except ImportError:
    kube = None


@app.route('/<webhook_name>/<webhook_key>', methods=['POST'])
def index(webhook_name, webhook_key):
    if config.webhooks[webhook_name] is None:
        print("Invalid wehbook name")
        abort(403)
    wh_config = config.webhooks[webhook_name]
    if not wh_config.is_key_valid(webhook_key):
        print(f"Invalid webhook key: {webhook_key}")
        print(f"Expected key: {wh_config._raw_config['key']}")
        abort(403)
    rq_json = request.get_json()
    if rq_json is None:
        print("Invalid JSON payload")
        abort(403)
    if "push_data" not in rq_json:
        print("No push_data in payload")
        abort(403)
    if "tag" not in rq_json["push_data"]:
        print("No tag found in push_data")
        abort(403)
    if rq_json["push_data"]["tag"] == "latest":
        return "That's cool and all but I don't care"
    print(rq_json)
    if kube is not None:
        namespace = wh_config["cluster"]["namespace"]
        label = wh_config["cluster"]["deployment_label"]
        return f"{kube.update_deployment_container_tag(namespace, label, rq_json['push_data']['tag'])}"
    return "Pogging"