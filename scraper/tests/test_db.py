from unittest import TestCase, mock

from mongomock import MongoClient

from db import add_post, get_post_by_external_id

client = MongoClient()
mocked_posts = client.database.posts


class DbTestCase(TestCase):

    def tearDown(self) -> None:
        mocked_posts.drop()

    @mock.patch('db.posts', mocked_posts)
    def test_adding_post(self):
        post = {
            'post_id': 1,
            'title': 'test',
            'url': 'test',
        }

        add_post(**post)

        self.assertEqual(mocked_posts.estimated_document_count(), 1)

    @mock.patch('db.posts', mocked_posts)
    def test_getting_post(self):
        post = {'external_id': 1}
        mocked_posts.insert_one(post)

        result = get_post_by_external_id(1)

        self.assertIsNotNone(result)
