from datetime import datetime
from server_flask.db import db


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'project.id', name='fk_project_id'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='fk_supplier_users_id'), nullable=False)
    # role = db.relationship('Role', secondary='supplier_role', backref='supplier')

