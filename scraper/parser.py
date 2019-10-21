import logging
from typing import Generator, Dict, Union, Optional
from urllib.parse import urlparse, urljoin

import requests
from lxml import html
from requests import RequestException

from db import get_post_by_external_id, add_post

logger = logging.getLogger(__name__)

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
        logger.error(f'An exception occurred while handling a request to {url}.')
        return
    if response.status_code != 200:
        logger.warning('Response status code is not successful')
        return
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
        raise StopIteration
    tree = html.fromstring(html_page)
    posts = tree.xpath(XPATH_POST_TR_ELEMENT)

    for post in posts:
        post_link = post.xpath(XPATH_POST_LINK_ELEMENT)[0]
        yield {
            'post_id': post.attrib['id'],
            'title': post_link.text,
            'url': cast_to_absolute_url(post_link.attrib['href']),
        }


def add_posts_into_db() -> int:
    added_posts_count = 0
    for post in get_posts():
        db_post = get_post_by_external_id(post['post_id'])
        if db_post is not None:
            continue
        add_post(
            post_id=post['post_id'],
            title=post['title'],
            url=post['url'],
        )
        added_posts_count += 1
    return added_posts_count
