import imp
from updater.config import webhook_config
from . import app
from . import config
from flask import request, abort
try:
    from . import kube
except ImportError:
    kube = None


@app.route('/<webhook_name>/<webhook_key>', methods=['GET', 'POST'])
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
    print(rq_json)
    if kube is not None:
        return f"{kube.get_pods()}"
    return "Pogging"