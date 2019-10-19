from typing import Generator, Dict, Union, Optional
from urllib.parse import urlparse, urljoin

import requests
from lxml import html
from requests import RequestException

PAGE_URL = 'https://news.ycombinator.com/'
XPATH_POST_TR_ELEMENT = '//*[contains(@class, \'athing\')]'
XPATH_POST_LINK_ELEMENT = './/*[contains(@class, \'storylink\')]'


def get_html_page(url: str) -> Optional[str]:
    """
    Attempts to request a page and returns response content
    """
    try:
        response = requests.get(url)
    except RequestException:
        # todo: logging
        return
    # todo: status != 200
    return response.text


def cast_to_absolute_url(url: str) -> str:
    """
    Returns absolute url if it is relative
    """
    if not urlparse(url).netloc:
        return urljoin(PAGE_URL, url)
    return url


def get_posts() -> Generator[Dict[str, Union[int, str]], None, None]:
    """
    Generator that returns posts from page as dict objects (id, title, url)
    """
    html_page = get_html_page(PAGE_URL)
    if html_page is None:
        raise
    tree = html.fromstring(html_page)
    posts = tree.xpath(XPATH_POST_TR_ELEMENT)

    for post in posts:
        post_link = post.xpath(XPATH_POST_LINK_ELEMENT)[0]
        yield {
            'post_id': post.attrib['id'],
            'title': post_link.text,
            'url': cast_to_absolute_url(post_link.attrib['href']),
        }
