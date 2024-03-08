from server_flask.db import db
from sqlalchemy.sql import func
class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_likes_users_id', ondelete="CASCADE"), nullable=False)
    posts_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', name='fk_likes_posts_id', ondelete="CASCADE"), nullable=True)
    orders_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_likes_orders_id', ondelete="CASCADE"), nullable=True)
    products_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', name='fk_likes_products_id', ondelete="CASCADE"), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey(
        'comment.id', name='fk_likes_comment_id', ondelete="CASCADE"), nullable=True)