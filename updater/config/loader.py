import os
from pathlib import Path
from time import sleep
import json
import threading
from .webhook_config import WebhookConfig


class ConfigLoader:
    def __init__(self):
        try:
            self.config_path = Path(os.environ.get("WEBHOOK_CONFIG_PATH"))
        except (KeyError, TypeError):
            print("Please provide the environment variable WEBHOOK_CONFIG_PATH to where the Flask app can find the config files for webhook processing")
            exit(1)
        self.running = None
        self._webhooks: Path = {}
        self.thread = threading.Thread(target=self._worker)
    
    def __getitem__(self, key):
        if key in self._webhooks:
            return self._webhooks[key]
        else:
            return None
    
    def _worker(self):
        while self.running:
            for file in self.config_path.iterdir():
                if file.name not in self._webhooks:
                    self._webhooks[file.name] = WebhookConfig()
                with file.open() as f:
                    self._webhooks[file.name]._raw_config = json.load(f)
                sleep(1)
            sleep(60)

    def start(self):
        if self.running is not None:
            return
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
