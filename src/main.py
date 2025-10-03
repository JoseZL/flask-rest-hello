from flask import request, jsonify
from models import db, User, Post, Comment, Like
from app import app

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.serialize() for post in posts]), 200

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(user_id=data['user_id'], image_url=data['image_url'], description=data.get('description'))
    db.session.add(post)
    db.session.commit()
    return jsonify(post.serialize()), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    data = request.get_json()
    post.image_url = data.get('image_url', post.image_url)
    post.description = data.get('description', post.description)
    db.session.commit()
    return jsonify(post.serialize()), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': 'Post deleted'}), 200

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    comment = Comment(user_id=data['user_id'], post_id=data['post_id'], text=data['text'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.serialize()), 201

@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    data = request.get_json()
    comment.text = data.get('text', comment.text)
    db.session.commit()
    return jsonify(comment.serialize()), 200

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'msg': 'Comment deleted'}), 200

@app.route('/likes', methods=['POST'])
def create_like():
    data = request.get_json()
    like = Like(user_id=data['user_id'], post_id=data['post_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify(like.serialize()), 201

@app.route('/likes/<int:like_id>', methods=['DELETE'])
def delete_like(like_id):
    like = Like.query.get(like_id)
    if not like:
        return jsonify({'error': 'Like not found'}), 404
    db.session.delete(like)
    db.session.commit()
    return jsonify({'msg': 'Like deleted'}), 200
