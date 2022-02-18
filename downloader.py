import re
import email.utils as eut
import datetime
from pathlib import Path
from typing import Optional, TypedDict
from playwright.sync_api import BrowserContext
import requests
import iso8601

from file import File


filename_regex = re.compile(r'filename="(.*)"')


def __get_filename_from_content_disposition(content_disposition) -> str:
    return filename_regex.search(content_disposition).group(1)


def __parse_date(date_str: str) -> datetime.datetime:
    return datetime.datetime(*eut.parsedate(date_str)[:6])


def __parse_date_rfc3339(date_str: str) -> datetime.datetime:
    return iso8601.parse_date(date_str)


class HeadResult(TypedDict, total=False):
    url: str
    filename: Optional[str]
    date: datetime.datetime
    last_modified: datetime.datetime
    content_type: str
    content_length: Optional[int]


def __get_cookie_jar_from_context(context: BrowserContext, url: str) -> requests.sessions.RequestsCookieJar:
    playwright_cookies = context.cookies(url)
    jar = requests.sessions.RequestsCookieJar()
    for cookie in playwright_cookies:
        jar.set(cookie["name"], cookie["value"],
                domain=cookie['domain'], path=cookie['path'])
    return jar


def head(context: BrowserContext, url: str, last_modified: datetime.datetime) -> HeadResult:
    jar = __get_cookie_jar_from_context(context, url)
    if url is None:
        return
    res = requests.head(url, cookies=jar, allow_redirects=True)

    if res.status_code not in [200, 302]:
        # TODO: log the error
        return

    content_length = res.headers.get('Content-Length')
    content_disposition = res.headers.get('Content-Disposition')
    last_modified = __parse_date(
        res.headers.get('Last-Modified')
    ) if 'Last-Modified' in res.headers else last_modified

    return {
        "url": url,
        "filename": __get_filename_from_content_disposition(content_disposition) if content_disposition else '',
        "date": __parse_date(res.headers['Date']),
        "last_modified": last_modified,
        "content_type": res.headers.get('Content-Type'),
        "content_length": int(content_length) if content_length else None
    }


def sync(context: BrowserContext, file: File):
    directory = Path(file.local_directory).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    __download_file(context, file.url, directory, __parse_date_rfc3339(file.date_modified))


def __check_if_downloaded(context: BrowserContext, url: str, directory: str, last_modified: datetime.datetime) -> bool:
    info = head(context, url, last_modified)
    if info is None:
        return True
    last_modified = info['last_modified']
    filename = info['filename']
    print(last_modified, filename)

    try:
        timestamp_modified = Path(directory, filename).stat().st_mtime
        return timestamp_modified > last_modified.timestamp()
    except:
        return False


def __download_file(context: BrowserContext, url: str, directory: str, last_modified: datetime.datetime):
    # don't download if already downloaded
    if __check_if_downloaded(context, url, directory, last_modified):
        return

    jar = __get_cookie_jar_from_context(context, url)

    res = requests.get(url, cookies=jar, stream=True)
    res.raise_for_status()
    # TODO: log the error

    filename = __get_filename_from_content_disposition(
        res.headers['Content-Disposition'])

    with Path(directory, filename).open('wb') as f:
        for chunk in res.iter_content(chunk_size=8192):
            f.write(chunk)
