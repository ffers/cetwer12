from datetime import datetime
from server_flask.db import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    project = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', name='fk_project_user_id'), nullable=False)