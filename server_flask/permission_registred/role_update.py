from flask import current_app
from flask_principal import identity_changed, Identity, identity_loaded, RoleNeed
from flask_security import current_user
from server_flask.models import Users
def update_roles():
    with current_app.app_context():
        identity_changed.send(current_app, identity=Identity(current_user.id))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Get the user information from the db
    if current_user.is_authenticated:
        id = current_user.id
        with current_app.app_context():
            user = Users.query.filter_by(id=id).first()
        # Update the roles that a user can provide
            for role in user.roles:
                identity.provides.add(RoleNeed(role.name))
        # Save the user somewhere so we only look it up once
        identity.user = user
