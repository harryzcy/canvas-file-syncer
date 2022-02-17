from msilib.schema import File
from typing import List
from playwright.sync_api import ElementHandle

from file import File


class Folder:
    def __init__(self, element: ElementHandle) -> None:
        self.__parent: Folder = None
        self.__subfolders: List[Folder] = []
        self.__files: List[File] = []

        self.__folder_name = element.get_attribute('aria-label')
        self.__level = int(element.get_attribute('aria-level'))
        self.__id = element.get_attribute('data-id')

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children

    @parent.setter
    def parent(self, value):
        self.parent: Folder = value

    @property
    def folder_name(self):
        return self.__folder_name

    def __get_subfolders(self, element: ElementHandle):
        els = element.query_selector_all(
            f'li[role="treeitem"][aria-level="{self.__level + 1}"]')
        self.__subfolders = [Folder(el) for el in els]
