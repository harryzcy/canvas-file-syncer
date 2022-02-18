from pathlib import Path, PurePath
import time
from typing import List
from playwright.sync_api import ElementHandle, Page

from file import File


class Folder:
    def __init__(self, page: Page, element: ElementHandle) -> None:
        self.__page = page

        self.__folder_name = element.get_attribute('aria-label')
        self.__level = int(element.get_attribute('aria-level'))
        self.__id = element.get_attribute('data-id')

        self.__root_path = ""
        self.__parent: Folder = None
        self.__subfolders: List[Folder] = []
        self.__files: List[File] = []

        self.__get_subfolders(element)

    @property
    def parent(self):
        return self.__parent

    @property
    def children(self):
        return self.__children

    @parent.setter
    def parent(self, value):
        self.__parent: Folder = value

    @property
    def folder_name(self):
        return self.__folder_name

    @property
    def root_path(self):
        return self.__root_path

    @root_path.setter
    def root_path(self, value):
        self.__root_path = str(Path(value).expanduser())

    @property
    def local_directory(self):
        if self.__parent is None:
            # is root if parent is None
            return self.__root_path
        dir = PurePath(self.parent.local_directory)
        dir = dir.joinpath(self.folder_name)
        return dir

    def __get_subfolders(self, element: ElementHandle):
        els = element.query_selector_all(
            f'li[role="treeitem"][aria-level="{self.__level + 1}"]')
        self.__subfolders = [Folder(self.__page, el) for el in els]
        for folder in self.__subfolders:
            folder.parent = self

    def __get_files(self):
        els = self.__page.locator(
            '.ef-directory .ef-item-row').element_handles()
        for el in els:
            size = el.query_selector('.ef-size-col').inner_text()
            if size != '--':
                # is file
                self.__files.append(File(self.__page, self, el))

    def __goto(self):
        with self.__page.expect_navigation():
            self.__page.locator(f'[data-id="{self.__id}"] > a').click()

    def walk(self):
        with self.__page.expect_navigation(wait_until='networkidle'):
            self.__goto()
            time.sleep(0.5)

        self.__get_files()
        for file in self.__files:
            yield file

        for folder in self.__subfolders:
            yield from folder.walk()
