from flask import Flask, jsonify

from db import Post
from schemas import PostsSchema

app = Flask(__name__)


@app.route('/posts')
def posts():
    posts_qs = Post.objects
    return jsonify(PostsSchema.dump(posts_qs))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
