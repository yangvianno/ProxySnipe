# config_loader.py

import yaml

def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)
    
config = load_config()
