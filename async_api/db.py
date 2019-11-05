import asyncio
from typing import Optional, List

import pymongo

from settings import DEFAULT_OFFSET, DEFAULT_LIMIT
from utils import init_mongo

db = init_mongo()


async def get_posts(
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    order: Optional[str] = None,
) -> List[dict]:
    posts = db.posts
    posts_cursor = posts.find().skip(offset).limit(limit)

    if order is not None:
        is_descending = order.startswith('-')
        direction = pymongo.DESCENDING if is_descending else pymongo.ASCENDING
        if is_descending:
            order = order[1:]
        posts_cursor = posts_cursor.sort([(order, direction)])

    return await posts_cursor.to_list(length=limit)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_posts())
