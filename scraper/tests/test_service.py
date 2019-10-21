from unittest import TestCase, mock

from nameko.testing.services import worker_factory

from services import Service

TEST_URL = 'http://example.com'


class ScraperServiceTestCase(TestCase):
    @mock.patch('services.add_posts_into_db', return_value=10)
    def test_parse_service(self, add_posts_into_db):
        service = worker_factory(Service)

        result = service.parse()

        self.assertTrue(add_posts_into_db.called)
        self.assertEqual(result, {'added': 10})
