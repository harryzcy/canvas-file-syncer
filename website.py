from typing import Callable, Any, Iterable
from playwright.sync_api import Page

from sites import Site


class Website():
    def __init__(self, page: Page, url: str, landing_url: str, login: Callable[[Page, str, str], Any]):
        self.__page = page
        self.__url = url
        self.__landing_url = landing_url
        self.__login = login

    def login(self):
        self.__login(self.__page, self.__url, self.__landing_url)

    def get_sites(page: Page) -> Iterable[Site]:
        """Get all sites on the current website."""
        cards = page.locator(
            '#DashboardCard_Container .ic-DashboardCard').element_handles()

        for card in cards:
            title = card.get_attribute('aria-label')
            href = card.query_selector(
                '.ic-DashboardCard__link').get_attribute('href')
            id = href.split("/")[-1]
            yield Site(page, id, title)

    def goto_site(self, site: Site):
        """Navigate to a site."""
        title = site.title
        with self.__page.expect_navigation():
            self.__page.locator(f'.ic-DashboardCard__header-title[title="{title}"]').click()
