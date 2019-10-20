from flask import Flask, jsonify
from flask import request
from nameko.standalone.rpc import ClusterRpcProxy

from db import Post
from schemas import PostsSchema, RequestArgsSchema
from settings import NAMEKO_CONFIG

app = Flask(__name__)


@app.route('/posts')
def posts():
    args = RequestArgsSchema.load(request.args)
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
    app.run(debug=True, host='0.0.0.0')
