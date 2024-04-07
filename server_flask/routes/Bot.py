from flask import Blueprint, render_template, request
import os
from flask_login import current_user
from dotenv import load_dotenv
from black import TelegramController

tg_cntrl = TelegramController()
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bp = Blueprint('Bot', __name__, template_folder='templates')

@bp.route("/bot", methods=['POST', 'GET'])
def bot():
    if request.method == 'POST':
        data = request.json
        print(request.json)
        try:
            tg_cntrl.await_tg_button(data)
        except:
            print("не вдалося отримати відповідь")
        return {'ok': True}
    return render_template('index.html', user=current_user)

