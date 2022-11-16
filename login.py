import time
from config import get_password, get_username
from playwright.sync_api import Page


def login(page: Page, url: str, landing_url: str):
    raise RuntimeError("default login not supported")


def login_unc(page: Page, url: str, landing_url: str) -> None:
    page.goto(url)

    page.wait_for_load_state('load')
    if page.url.startswith(landing_url):
        return

    with page.expect_navigation():
        page.locator('text="Onyen Login"').click()

    if page.url.startswith(landing_url):
        page.click("text=Not Now")
        page.click("text=Done")
        return

    page.locator(
        "text=Onyen -or- UNC Guest ID Loading... Next Important This browser does not support  >> input[name=\"j_username\"]").fill(get_username())
    page.locator("text=Loading... Next").click()
    page.locator(
        "text=Password Loading... Sign in Change Onyen -or- UNC Guest ID >> input[name=\"j_password\"]").fill(get_password())

    with page.expect_navigation(url=landing_url):
        page.locator("text=Loading... Sign in").click()
    page.click("text=Not Now")
    page.click("text=Done")


def login_kenan_flagler(page: Page, url: str, landing_url: str) -> None:
    page.goto(url)

    page.wait_for_load_state('load')
    if page.url.startswith(landing_url):
        return

    with page.expect_navigation():
        page.locator("text=ONYEN Login").click()

    time.sleep(0.5)
    page.locator("input[type=email]").fill(get_username())
    with page.expect_navigation():
        page.locator("input[type=submit]").click()

    time.sleep(1)
    page.locator("input[type=password]").fill(get_password())
    with page.expect_navigation():
        page.click('input[type=submit]')

    if page.url.endswith("/login"):
        # 2-factor auth
        page.locator("div[role=\"button\"]:has-text(\"Text\")").click()

        print("Enter code: ", end="")
        code = input()
        code = code.strip()

        page.locator("[aria-label=\"Code\"]").fill(code)
        with page.expect_navigation():
            page.locator("text=Verify").click()
        page.locator("[aria-label=\"Don\\'t\\ show\\ this\\ again\"]").check()
        page.locator("text=Yes").click()

    time.sleep(0.5)
    assert page.url.startswith(landing_url)
