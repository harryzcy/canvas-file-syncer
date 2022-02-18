import os
from typing import Dict, List
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
        if config is None:
            print('failed to load the configuration file')
            exit(1)


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


def get_cookies_filepath() -> str:
    return config.get('cookies').get('filepath')


def get_websites() -> List[str]:
    return config.get('websites').keys()


def get_website_config(website_name: str, field: str):
    website = config['websites'][website_name]
    if field in website:
        return website[field]
    return config['websites']['default'][field]
