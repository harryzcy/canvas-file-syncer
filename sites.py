from playwright.sync_api import Page

from folder import Folder


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

    def goto_files(self):
        """Navigate to files tab in the current site."""
        assert self.__page.url.endswith(self.id)
        with self.__page.expect_navigation():
            self.__page.locator('#section-tabs .section .files').click()

    def get_folders(self) -> Folder:
        """Returns the root folder that contains all other folders"""
        root_folder = self.__page.locator('.ef-folder-list li[aria-level="1"]')
        element = root_folder.element_handle()
        return Folder(element)
