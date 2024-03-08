import logging, psycopg2, os, threading, datetime
from celery import Celery
from flask import Flask, render_template, request
from flask_login import current_user, LoginManager, login_required
from flask_migrate import Migrate
from .db import db
from .routes import Blog, Auth, Comment, User_post, Bot, Order, Cabinet, Admin, Products
from dotenv import load_dotenv
from flask_principal import identity_loaded, RoleNeed, Principal, Identity, identity_changed
from server_flask.permission_registred import update_roles

load_dotenv()
app = Flask(__name__)
principal = Principal(app)
migrate = Migrate(app, db, directory='../common_asx/migrations')
user_db = os.getenv('DB_USERNAME')
password_db = os.getenv('DB_PASSWORD')

app.logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('flask.log')
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_FLASK")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user_db}:{password_db}@localhost:5432/flask_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # URL для брокера повідомлень (може бути Redis або інший)
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # URL для збереження результатів завдань

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
db.init_app(app)
celery.conf.update(app.config)
app.register_blueprint(Blog)
app.register_blueprint(Auth)
app.register_blueprint(Comment)
app.register_blueprint(User_post)
app.register_blueprint(Bot)
app.register_blueprint(Order)
app.register_blueprint(Cabinet)
app.register_blueprint(Admin)
app.register_blueprint(Products)


from .models import Users
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='flask_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.json)
        return {'ok':True}
    print(f"Hello Task Celery !!!!!")
    # identity_changed.send(app, identity=Identity(current_user.id))
    # print(current_user.id)
    return render_template('index.html', user=current_user)

@identity_loaded.connect_via(app)
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



