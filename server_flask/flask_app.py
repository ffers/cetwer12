from .app import app
from celery import Celery
import psycopg2, os
from dotenv import load_dotenv
from markupsafe import escape
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template, request, jsonify
from flask_login import current_user, LoginManager, login_required
from flask_migrate import Migrate
from flask_principal import identity_loaded, RoleNeed, Principal, Identity
from server_flask.permission_registred import update_roles
from .db import db
from .routes import Blog, Auth, Comment, User_post, Bot, \
    Order, Cabinet, Admin, Products, Analitic, \
    Arrival, JourChRout, ProductSource, SourceDifference
from utils import util_asx
OC_log = util_asx.oc_log("flas_app")

load_dotenv()
try:
    flask_app = Flask(__name__)
except Exception as e:
    # Запис повідомлення про помилку у журнал
    OC_log.exception("Помилка при створенні екземпляра додатку: %s", e)

principal = Principal(flask_app)
migrate = Migrate(flask_app, db, directory='../common_asx/migrations')
user_db = os.getenv('DB_USERNAME')
password_db = os.getenv('DB_PASSWORD')

flask_app.config['SECRET_KEY'] = os.getenv("SECRET_KEY_FLASK")
flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user_db}:{password_db}@localhost:5432/flask_db"
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config["SQLALCHEMY_ECHO"] = False
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
flask_app.register_blueprint(Analitic)
flask_app.register_blueprint(Arrival)
flask_app.register_blueprint(JourChRout)
flask_app.register_blueprint(ProductSource)
flask_app.register_blueprint(SourceDifference)

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
@login_required
def index():
    if request.method == 'POST':
        print(request.json)
        return {'ok':True}
    print(f"{current_user.is_authenticated}")
    return render_template('index.html', user=current_user)


@flask_app.route("/health-check") 
def health_check():
    return "OK1", 200

@flask_app.errorhandler(403)
def handle_forbidden_error(error):
    # Рендеринг шаблону для виведення зображення або повідомлення про помилку
    return render_template('403.html'), 403

@flask_app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@identity_loaded.connect_via(flask_app)
def on_identity_loaded(sender, identity):
    # Get the user information from the db
    if current_user.is_authenticated:
        id = current_user.id
        user = Users.query.filter_by(id=id).first()
        # Update the roles that a user can provide
        for role in user.roles:
            identity.provides.add(RoleNeed(role.name))
        # Save the user somewhere so we only look it up once
        identity.user = user
        update_roles()

@flask_app.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify({'message': str(error)})
    response.status_code = 400  # Встановлення коду статусу відповіді
    return response

@principal.identity_loader
def load_indentity_session():
    if hasattr(current_user, 'id'):
        return Identity(current_user.id)

# @celery.task
# def schedule_task():
#     schedule.every(3).seconds.do(st_del_script.load_track)
#     print("Calary")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# schedule_task()



try:
    app.mount("/", WSGIMiddleware(flask_app))
except Exception as e:
    # Запис повідомлення про помилку у журнал
    OC_log.exception("Помилка при монтуванні flask_app: %s", e)

