from typing import Callable, Any
from playwright.sync_api import Page


class Website():
    def __init__(self, page: Page, url: str, landing_url: str, login: Callable[[Page, str, str], Any]):
        self.__page = page
        self.__url = url
        self.__landing_url = landing_url
        self.__login = login

    def login(self):
        self.__login(self.__page, self.__url, self.__landing_url)
