from flask import Flask, jsonify
from flask import request
from db import Post
from schemas import PostsSchema, RequestArgsSchema

app = Flask(__name__)


@app.route('/posts')
def posts():
    args = RequestArgsSchema.load(request.args)
    posts_qs = (
        Post.objects
            .order_by(args.get('order'))
            .skip(args.get('offset'))
            .limit(args.get('limit'))
    )
    return jsonify(PostsSchema.dump(posts_qs))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
