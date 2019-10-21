from flask import Flask, jsonify
from flask import request
from marshmallow import ValidationError
from nameko.standalone.rpc import ClusterRpcProxy

from db import Post
from schemas import PostsSchema, RequestArgsSchema
from settings import NAMEKO_CONFIG

app = Flask(__name__)


@app.route('/posts')
def posts():
    try:
        args = RequestArgsSchema.load(request.args)
    except ValidationError as err:
        return (
            jsonify({
                'error': 'BAD_REQUEST',
                'message': err.messages,
            }),
            400,
        )
    if args.get('action'):
        with ClusterRpcProxy(NAMEKO_CONFIG) as rpc:
            result = rpc.scraper_service.parse()
        return result
    posts_qs = (
        Post.objects
            .order_by(args.get('order'))
            .skip(args.get('offset'))
            .limit(args.get('limit'))
    )
    return jsonify(PostsSchema.dump(posts_qs))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
