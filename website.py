from typing import Callable, Any, Iterable
from playwright.sync_api import Page

from sites import Site


class Website():
    def __init__(self, page: Page, url: str, landing_url: str, login: Callable[[Page, str, str], Any]):
        self.__page = page
        self.__url = url
        self.__landing_url = landing_url
        self.__login = login
        self.__sites = None

    def login(self):
        self.__login(self.__page, self.__url, self.__landing_url)

    def get_sites(self) -> Iterable[Site]:
        """Get all sites on the current website."""
        if self.__sites is not None:
            return self.__sites

        cards = self.__page.locator(
            '#DashboardCard_Container .ic-DashboardCard').element_handles()

        for card in cards:
            title = card.get_attribute('aria-label')
            href = card.query_selector(
                '.ic-DashboardCard__link').get_attribute('href')
            id = href.split("/")[-1]
            yield Site(self.__page, id, title)
    
    def get_site(self, title: str) -> Site:
        """Get a site by title."""
        for site in self.get_sites():
            if site.title == title:
                return site
        return None

    def goto_site(self, site: Site):
        """Navigate to a site."""
        title = site.title
        with self.__page.expect_navigation():
            self.__page.locator(f'.ic-DashboardCard__header-title[title="{title}"]').click()
