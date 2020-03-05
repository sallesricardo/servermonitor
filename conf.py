import ujson as json
import os
from uuid import uuid4 as uuid

class Conf:
    brand = "Brand"
    favicon = "icon.ico"
    sm_logo = "sm_logo.png"
    secret_key = str(uuid())

    def __init__(self, config_file="config.json"):
        if os._exists(config_file):
            with open(config_file, 'r') as config:
                data = json.load(config)

            if 'brand' in data:
                self.brand = data['brand']
            
            if 'favicon' in data:
                self.favicon = data['favicon']

            if 'sm_logo' in data:
                self.sm_logo = data['sm_logo']        

            if 'secret_key' in data:
                self.secret_key = data['secret_key']        