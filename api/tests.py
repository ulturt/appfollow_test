import unittest
from datetime import datetime

from mongoengine import connect, disconnect

from app import app
from db import Post
from factories import PostFactory


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def setUp(self) -> None:
        self.app = app.test_client()

    def tearDown(self) -> None:
        Post.drop_collection()

    def test_posts_with_empty_db(self):
        response = self.app.get('/posts')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_posts_with_posts_in_db(self):
        posts_count = 10
        PostFactory.create_batch(posts_count)

        response = self.app.get('/posts')

        self.assertEqual(len(response.json), posts_count)

    def test_post_fields(self):
        post = PostFactory(
            external_id=1,
            title='test',
            url='http://example.com',
            created=datetime(2000, 1, 1),
        )

        response = self.app.get('/posts')

        self.assertEqual(
            response.json,
            [self.get_post_as_dict(post)],
        )

    def test_ordering(self):
        posts = PostFactory.create_batch(3)

        response = self.app.get('/posts?order=-title')

        sorted_posts = sorted(posts, key=lambda x: x.title, reverse=True)
        self.assertEqual(
            list(map(lambda x: x['title'], response.json)),
            [post.title for post in sorted_posts],
        )

    def test_limit(self):
        posts_count = 10
        limit = 5
        posts = PostFactory.create_batch(posts_count)

        response = self.app.get(f'/posts?limit={limit}')

        self.assertEqual(
            list(map(lambda x: x['id'], response.json)),
            [post.external_id for post in posts][:limit],
        )

    def test_offset(self):
        posts_count = 10
        offset = 5
        posts = PostFactory.create_batch(posts_count)

        response = self.app.get(f'/posts?offset={offset}')

        self.assertEqual(
            list(map(lambda x: x['id'], response.json)),
            [post.external_id for post in posts][offset:],
        )

    @staticmethod
    def get_post_as_dict(post):
        return {
            'id': post.external_id,
            'title': post.title,
            'url': post.url,
            'created': post.created.replace(tzinfo=None).isoformat(),
        }
