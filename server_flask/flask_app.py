# from server_fast.app import app
from .db import db

import psycopg2, os
from markupsafe import escape

from flask import Flask, render_template, request, jsonify, abort
from flask_login import current_user, LoginManager, login_required
from flask_migrate import Migrate
from flask_principal import identity_loaded, RoleNeed
from flask_principal import Principal, Identity
from server_flask.permission_registred import update_roles
from .security_middleware import security_blocker

from .routes import Blog, Auth, Comment, User_post, Bot, \
    Order, Cabinet, Admin, Products, Analitic, \
    Arrival, JourChRout, ProductSource, SourceDifference, \
    ColorSource, Panel, Store, Crm, PayMethod, \
    Balance, Delivery



from celery import Celery
from dotenv import load_dotenv

from utils import OC_logger

load_dotenv()


logger = OC_logger.oc_log("flask_app")
logger_access = OC_logger.oc_log("access_flask")


try:
    flask_app = Flask(__name__)
except Exception as e:
    # Запис повідомлення про помилку у журнал
    logger.exception("Помилка при створенні екземпляра додатку: %s", e)

security_blocker(flask_app)
principal = Principal(flask_app)
migrate = Migrate(flask_app, db, directory='../common_asx/migrations')
user_db = os.getenv('DB_USERNAME')
password_db = os.getenv('DB_PASSWORD')

flask_app.config['DEBUG'] = True if os.getenv("ENV") == "dev" else False
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
flask_app.register_blueprint(ColorSource, url_prefix='/cabinet/source')
flask_app.register_blueprint(Panel, url_prefix='/cabinet/workspace')
flask_app.register_blueprint(Store, url_prefix='/cabinet/store')
flask_app.register_blueprint(PayMethod, url_prefix='/cabinet/pay_method')
flask_app.register_blueprint(Crm, url_prefix='/crm')
flask_app.register_blueprint(Balance, url_prefix='/balance')
flask_app.register_blueprint(Delivery, url_prefix='/delivery')

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

@flask_app.before_request
def log_request():
    pass
    # logger_access.info(
    #     f"{request.remote_addr} {request.method} {request.path} "
    #     f"params={dict(request.args)} agent={request.headers.get('User-Agent')}"
    # )

@flask_app.before_request
def block_bots():
    ua = request.headers.get("User-Agent", "").lower()
    path = request.path.lower()
    if (
        "phpunit" in path or "think" in path or "zgrab" in ua or
        "async" in ua or "wlwmanifest" in path or "ecp" in path
    ):
        return "⛔ Заборонено", 403

# @flask_app.after_request
# def log_response(response):
#     response.direct_passthrough = False

#     log_data = {
#         "status": response.status_code,
#         "path": request.path,
#         "method": request.method,
#         "response": response.get_data(as_text=False).decode("utf-8", errors="replace")[:500]
#     # обрізано
#     }
#     logger.info(f"API response: {log_data}")
#     return response

@flask_app.before_request
def detect_scanning():
    path = request.path
    agent = request.headers.get("User-Agent", "")
    if is_suspicious_request(path, agent):
        msg = f"`{request.remote_addr}` запитав `{path}`\n🕵 Agent: `{agent}`"
        send_telegram_alert(msg)


import os
import requests

SUSPICIOUS_PATHS = [
    "/actuator", "/.vscode", "/debug", "/fgt_lang", "/phpinfo", "/ecp", "/remote"
]

SUSPICIOUS_AGENTS = [
    "Go-http-client", "sqlmap", "acunetix", "crawler"
]


def send_telegram_alert(text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID_INFO")
    if not token or not chat_id:
        return
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": f"🚨 *Security Alert!*\n{text}", "parse_mode": "Markdown"}
    )

def is_suspicious_request(path, user_agent):
    return (
        any(p in path for p in SUSPICIOUS_PATHS) or
        any(agent.lower() in user_agent.lower() for agent in SUSPICIOUS_AGENTS)
    )



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
    if request.accept_mimetypes['application/json']:
        return jsonify({"Forbidden": "You do not have permission to access this resource."}), 403
    # Рендеринг шаблону для виведення зображення або повідомлення про помилку
    return render_template('403.html'), 403

@flask_app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes['application/json']:
        return jsonify({"error": "Page not found"}), 404
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
    
@flask_app.errorhandler(TypeError)
def handle_type_error(e):
    import traceback
    traceback.print_exc()
    return {"error": str(e)}, 500

BLOCKED_PATHS = [
    ".env", ".git", ".aws", ".docker", ".idea", "config", "backup",
    ".env.local", ".env.dev", ".env.prod", ".env.test", ".env.stage",
    ".env.backup", ".env.dist", ".env.ci", ".git/config", ".aws/credentials"
]

def security_blocker(app):
    @app.before_request
    def block_suspicious_paths():
        path = request.path.lower()
        for bad in BLOCKED_PATHS:
            if bad in path:
                abort(403)


# @celery.task
# def schedule_task():
#     schedule.every(3).seconds.do(st_del_script.load_track)
#     print("Calary")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# schedule_task()





