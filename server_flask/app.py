import logging, psycopg2, os, threading, datetime
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from celery import Celery
from flask import Flask, render_template, request
from markupsafe import escape

from flask_login import current_user, LoginManager, login_required
from flask_migrate import Migrate
from .db import db
from .routes import Blog, Auth, Comment, User_post, Bot, Order, Cabinet, Admin, Products
from dotenv import load_dotenv
from flask_principal import identity_loaded, RoleNeed, Principal, Identity, identity_changed
from server_flask.permission_registred import update_roles

load_dotenv()
flask_app = Flask(__name__)
principal = Principal(flask_app)
migrate = Migrate(flask_app, db, directory='../common_asx/migrations')
user_db = os.getenv('DB_USERNAME')
password_db = os.getenv('DB_PASSWORD')

flask_app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.INFO)
flask_app.logger.addHandler(file_handler)

flask_app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_FLASK")
flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user_db}:{password_db}@localhost:5432/flask_db"
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config["SQLALCHEMY_ECHO"] = True
flask_app.config["SQLALCHEMY_RECORD_QUERIES"] = True
flask_app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # URL для брокера повідомлень (може бути Redis або інший)
flask_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # URL для збереження результатів завдань

celery = Celery(flask_app.name, broker=flask_app.config['CELERY_BROKER_URL'])
db.init_app(flask_app)
celery.conf.update(flask_app.config)
flask_app.register_blueprint(Blog)
flask_app.register_blueprint(Auth)
flask_app.register_blueprint(Comment)
flask_app.register_blueprint(User_post)
flask_app.register_blueprint(Bot)
flask_app.register_blueprint(Order)
flask_app.register_blueprint(Cabinet)
flask_app.register_blueprint(Admin)
flask_app.register_blueprint(Products)


from .models import Users
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(flask_app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@flask_app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.json)
        return {'ok':True}
    print(f"Hello Task Celery !!!!!")
    # identity_changed.send(flask_app, identity=Identity(current_user.id))
    # print(current_user.id)
    return render_template('index.html', user=current_user)

@identity_loaded.connect_via(flask_app)
def on_identity_loaded(sender, identity):
    # Get the user information from the db
    print("INDENTITY LOAD")
    if current_user.is_authenticated:
        print("USER AUTHENTICATED")
        id = current_user.id
        user = Users.query.filter_by(id=id).first()
        # Update the roles that a user can provide
        for role in user.roles:
            identity.provides.add(RoleNeed(role.name))
        # Save the user somewhere so we only look it up once
        identity.user = user
        update_roles()

@principal.identity_loader
def load_indentity_session():
    if hasattr(current_user, 'id'):
        return Identity(current_user.id)

app = FastAPI()

@app.get("/v2")
def read_main():
    return {"message": "Hello World"}


app.mount("/", WSGIMiddleware(flask_app))



