from playwright.sync_api import Page


class File:
    def __init__(self, page: Page, id: str, title: str) -> None:
        self.__page = page
