from updater.config import webhook_config
from . import app
from . import config
from flask import request, abort
# from . import kube


@app.route('/<webhook_name>/<webhook_key>')
def index(webhook_name, webhook_key):
    if config.webhooks[webhook_name] is None:
        abort(403)
    wh_config = config.webhooks[webhook_name]
    if not wh_config.is_key_valid(webhook_key):
        abort(403)
    rq_json = request.get_json()
    print(rq_json)
    # return f"{kube.get_pods()}"
    return "Pogging"