import requests
from lxml import html
from requests import RequestException

PAGE_URL = 'https://news.ycombinator.com/'
XPATH_POST_TR_ELEMENT = '//*[contains(@class, \'athing\')]'
XPATH_POST_LINK_ELEMENT = './/*[contains(@class, \'storylink\')]'


def get_html_page(url):
    try:
        response = requests.get(url)
    except RequestException:
        # todo: logging
        return
    # todo: status != 200
    return response.text


def get_posts():
    html_page = get_html_page(PAGE_URL)
    if html_page is None:
        raise
    tree = html.fromstring(html_page)

    posts = tree.xpath(XPATH_POST_TR_ELEMENT)
    for post in posts:
        post_id = post.attrib['id']
        post_link = post.xpath(XPATH_POST_LINK_ELEMENT)[0]
        post_title = post_link.text
        post_url = post_link.attrib['href']

        yield post_id, post_title, post_url
