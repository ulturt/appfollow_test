from aiohttp import web
from marshmallow import ValidationError

from db import get_posts
from schemas import posts_schema, posts_request_schema

routes = web.RouteTableDef()


@routes.get('/posts')
async def posts(request):
    try:
        query_params = posts_request_schema.load(request.query)
    except ValidationError as err:
        return web.json_response(
            data=err.messages,
            status=400,
        )

    posts_list = await get_posts(**query_params)
    data = posts_schema.dump(posts_list)
    return web.json_response(data)


if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    web.run_app(
        app=app,
        port=5000,
    )
