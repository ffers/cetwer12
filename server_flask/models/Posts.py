from datetime import datetime
from server_flask.db import db

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    name_post = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_posts_users_id', ondelete="CASCADE"), nullable=True)
    comments = db.relationship('Comment', backref='posts', passive_deletes=True)
    likes = db.relationship('Likes', backref='posts', passive_deletes=True)

