
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from server_flask.db import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_comment_users_id', ondelete="CASCADE"), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', name='fk_comment_posts_id',  ondelete="CASCADE"), nullable=True)
    orders_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_comment_orders_id', ondelete="CASCADE"), nullable=True)
    replies = db.relationship('Reply', back_populates='comment')
    likes = db.relationship('Likes', backref='comment', passive_deletes=True)


