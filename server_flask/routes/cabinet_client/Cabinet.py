from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from server_flask.models import  Users, Orders
from flask_login import login_required, current_user
from server_flask.db import db
from flask_principal import Permission, RoleNeed

manager = RoleNeed('manager')
author_permission = Permission(manager)
bp = Blueprint('Cabinet', __name__, template_folder='templates')

@bp.route('/cabinet', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def Cabinet():
    if request.method == 'POST':

        print(">>> Add datebase")
        return redirect('/orders')
    else:
        tasks_orders = Orders.query.order_by(Orders.timestamp).all()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        return render_template('cabinet_client/cabinet.html', tasks_users=tasks_users, orders=tasks_orders,  user=current_user)