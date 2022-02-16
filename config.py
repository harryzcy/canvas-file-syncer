import os
import yaml


config = {}

DEFAULT_CONFIG_FILE = "config.yaml"

def init(filename: str | None = DEFAULT_CONFIG_FILE):
    """initialize configurations"""
    if filename is None:
        filename = DEFAULT_CONFIG_FILE

    with open(filename, 'r') as stream:
        global config
        config = yaml.safe_load(stream)


def get_username():
    username = os.getenv('CANVAS_USERNAME')
    if not username:
        print('CANVAS_USERNAME not specified')
        exit(1)
    return username


def get_password():
    password = os.getenv('CANVAS_PASSWORD')
    if not password:
        print('CANVAS_PASSWORD not specified')
        exit(1)
    return password
