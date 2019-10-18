from mongoengine import (
    StringField,
    Document,
    connect,
    URLField,
    IntField,
    DateTimeField,
)

connect('database', host='db', port=27017)


class Post(Document):
    external_id = IntField()
    title = StringField()
    url = URLField()
    created = DateTimeField()

    meta = {'collection': 'posts'}
