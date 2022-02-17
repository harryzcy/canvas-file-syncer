from playwright.sync_api import Page, ElementHandle

from folder import Folder


class File:
    def __init__(self, page: Page, parent: Folder, element: ElementHandle):
        self.__page = page
        self.__parent = parent
        self.__element = element

        self.__filename = element.query_selector(
            '.ef-name-col__text').inner_text()
        self.__date_created = element.query_selector(
            '.ef-date-created-col time').get_attribute('datetime')
        self.__date_modified = element.query_selector(
            '.ef-date-modified-col time').get_attribute('datetime')
        self.__size = element.query_selector('.ef-size-col').inner_text()
        self.__url = element.query_selector(
            '.ef-name-col > a').get_attribute('href')
    
    @property
    def local_directory(self):
        return self.__parent.local_directory

    @property
    def url(self):
        return self.__url