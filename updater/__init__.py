import threading
from flask import Flask
import atexit
from . import config


def create_app():
    app = Flask(__name__)
    def interrupt():
        config.webhooks.stop()
    config.webhooks.start()
    atexit.register(interrupt)
    return app
app = create_app()
from . import views
