import os
import sys
from typing import Any, Callable
from playwright.sync_api import Playwright, Page, sync_playwright

import config
import login
from website import Website


def start(playwright: Playwright, debug=False) -> Page:
    browser = playwright.chromium.launch(headless=not debug)
    context = browser.new_context()
    page = context.new_page()

    return page


def finish(page: Page):
    page.close()
    page.context.close()
    page.context.browser.close()


def main(debug=False):
    websites = config.get_websites()

    with sync_playwright() as p:
        page = start(p, debug=debug)

        for name in websites:
            if name == 'default':
                continue

            login_func: Callable[[Page, str, str], Any] = getattr(
                login,
                config.get_website_config(name, 'login_func')
            )
            website = Website(page,
                              url=config.get_website_config(name, 'url'),
                              landing_url=config.get_website_config(
                                  name, 'landing_url'),
                              login=login_func)

            website.login()

            sites = website.get_sites()
            for site in sites:
                site.goto_files()
                folder = site.get_folders()
                folder.root_path = config.get_website_config(
                    name, 'download-directory')

        finish(page)


if __name__ == "__main__":
    # python version at least 3.7
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 7

    debug_env = os.getenv("DEBUG")
    debug = debug_env == 'true'

    config_path = os.getenv("CONFIG_PATH")
    config.init(config_path)

    main(debug=debug)
