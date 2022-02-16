import os
import sys
from playwright.sync_api import Playwright, Page, sync_playwright

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
    with sync_playwright() as p:
        page = start(p, debug=debug)

        finish(page)

if __name__ == "__main__":
    # python version at least 3.7
    assert sys.version_info.major == 3
    assert sys.version_info.minor >= 7

    debug_env = os.getenv("DEBUG")
    debug = debug_env == 'true'

    main(debug=debug)
