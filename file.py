from playwright.sync_api import Page, ElementHandle


class File:
    def __init__(self, page: Page, element: ElementHandle):
        self.__page = page
        self.__element = element

    def download(self):
        pass
