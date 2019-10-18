import datetime

from pymongo import MongoClient

client = MongoClient('db')
db = client.database
posts = db.posts


def get_post_by_external_id(post_id):
    return posts.find_one({'external_id': post_id})


def add_post(post_id, title, url):
    post = {
        'external_id': post_id,
        'title': title,
        'url': url,
        'created': datetime.datetime.utcnow(),
    }
    posts.insert_one(post)
