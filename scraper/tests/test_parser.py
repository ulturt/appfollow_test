import os
from unittest import mock
from unittest.case import TestCase

import requests_testing

from parser import get_html_page, logger, cast_to_absolute_url, get_posts, add_posts_into_db
from tests.test_db import mocked_posts
from tests.test_service import TEST_URL


class ParserTestCase(TestCase):
    @requests_testing.activate
    def test_get_html_page_success(self):
        requests_testing.add(request={'url': TEST_URL}, response={'body': 'test'})

        result = get_html_page(TEST_URL)

        self.assertEqual(result, 'test')

    @requests_testing.activate
    def test_get_html_page_error(self):
        with self.assertLogs(logger=logger, level='ERROR') as logs:
            result = get_html_page(TEST_URL)

            self.assertIsNone(result)
            self.assertEqual(len(logs.output), 1)

    @requests_testing.activate
    def test_get_html_page_success(self):
        requests_testing.add(request={'url': TEST_URL}, response={'status': 403})

        with self.assertLogs(logger=logger, level='WARNING') as logs:
            result = get_html_page(TEST_URL)

            self.assertIsNone(result)
            self.assertEqual(len(logs.output), 1)

    def test_cast_to_absolute_url_with_abs_url(self):
        result = cast_to_absolute_url(TEST_URL)

        self.assertEqual(result, TEST_URL)

    @mock.patch('parser.PAGE_URL', TEST_URL)
    def test_cast_to_absolute_url_with_relative_url(self):
        relative_url = '/test'

        result = cast_to_absolute_url(relative_url)

        self.assertEqual(result, TEST_URL + relative_url)

    @requests_testing.activate
    @mock.patch('parser.PAGE_URL', TEST_URL)
    def test_get_posts_with_parsed_page(self):
        path_to_file = os.path.join(os.path.dirname(__file__), 'test_page.html')
        with open(path_to_file) as test_file:
            test_page = test_file.read()
        requests_testing.add(request={'url': TEST_URL}, response={'body': test_page})

        gen = get_posts()

        post = next(gen)
        self.assertEqual(
            post,
            {
                'post_id': '21306597',
                'title': 'The Grove 8 â€“ Growing Trees in Blender',
                'url': 'https://www.thegrove3d.com/releases/the-grove-release-8/'
            }
        )

    @mock.patch('db.posts', mocked_posts)
    def test_add_posts_into_db(self):
        posts = [{
            'post_id': 1,
            'title': 'test',
            'url': 'url',
        }]

        with mock.patch('parser.get_posts', return_value=posts):
            result = add_posts_into_db()

        self.assertEqual(mocked_posts.estimated_document_count(), 1)
        self.assertEqual(result, 1)
