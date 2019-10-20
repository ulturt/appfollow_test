from db import get_post_by_external_id, add_post
from parser import get_posts


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


if __name__ == '__main__':
    add_posts_into_db()
