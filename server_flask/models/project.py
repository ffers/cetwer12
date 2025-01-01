from datetime import datetime
from server_flask.db import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_project_user_id'), nullable=False)