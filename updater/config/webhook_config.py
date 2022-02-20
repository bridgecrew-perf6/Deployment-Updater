import json
import os


class WebhookConfig:
    def __init__(self, json_text=None):
        if json_text is not None and isinstance(json_text, str):
            self._raw_config = json.loads(json_text)
        else:
            self._raw_config = json_text
    
    def is_key_valid(self, key_to_test):
        if 'key' not in self._raw_config:
            return False
        the_key: str = self._raw_config['key']
        if the_key is None:
            return False
        match = True
        for i in range(len(the_key)):
            try:
                match &= the_key[i] == key_to_test[i]
            except IndexError:
                match = False
        return match
    
    @property
    def cluster_namespace(self):
        if "cluster" not in self._raw_config:
            return None
        if "namespace" not in self._raw_config["cluster"]:
            return None
        return self._raw_config["cluster"]["namespace"]
    
    @property
    def cluster_deployment_label(self):
        if "cluster" not in self._raw_config:
            return None
        if "deployment_label" not in self._raw_config["cluster"]:
            return None
        return self._raw_config["cluster"]["deployment_label"]
    
    @property
    def cluster_tag(self):
        if "cluster" not in self._raw_config:
            return "latest"
        if "tag" not in self._raw_config["cluster"]:
            return "latest"
        return self._raw_config["cluster"]["tag"]
