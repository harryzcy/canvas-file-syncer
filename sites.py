from playwright.sync_api import Page


class Site:
    def __init__(self, page: Page, id: str, title: str) -> None:
        self.__page = page
        self.__id = id
        self.__title = title
    
    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        return self.__title

