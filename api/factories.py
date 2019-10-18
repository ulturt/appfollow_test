from datetime import datetime

from dateutil.tz import UTC
from factory import sequence
from factory.fuzzy import FuzzyDateTime
from factory.mongoengine import MongoEngineFactory

from db import Post


class PostFactory(MongoEngineFactory):
    external_id = sequence(lambda x: x)
    title = sequence(lambda x: f'title_{x}')
    url = sequence(lambda x: f'http://{x}.example.com')
    created = FuzzyDateTime(start_dt=datetime(2000, 1, 1, tzinfo=UTC))

    class Meta:
        model = Post
