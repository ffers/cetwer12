from flask import Blueprint, render_template, request, jsonify
import os
from flask_login import current_user
from dotenv import load_dotenv
from black.tg_answer_cntrl import TgAnswerCntrl
from black.order_cntrl import OrderCntrl

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bp = Blueprint('Bot', __name__, template_folder='templates')

@bp.route("/bot", methods=['POST', 'GET'])
def bot():
    if request.method == 'POST':
        tg = TgAnswerCntrl(OrderCntrl())
        data = request.json
        # try:
        tg.await_tg_button(data)
        # except:
        #     print("не вдалося отримати відповідь")
        return {'success': True}
    return render_template('index.html', user=current_user)

# @bp.route("/bot_send", methods=['POST', 'GET'])
# def bot_send():
#     tg_cntrl.sendPhoto()
#     return jsonify({'success': True})

