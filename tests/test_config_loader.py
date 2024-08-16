import pytest
from exodus.config.config_loader import ConfigLoader

def test_load_config():
    config_loader = ConfigLoader("config.yaml")
    config = config_loader.load_config()
    assert 'backup' in config
    assert 'cloud' in config
    assert 'webserver' in config