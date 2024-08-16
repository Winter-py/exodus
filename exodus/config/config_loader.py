import yaml
import os

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file {self.config_path} not found.")
        
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        # Validate the config if needed
        return config
