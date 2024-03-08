from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for, jsonify, session
from server_flask.models import Comment, Posts, Reply, Reply2, Users, Orders, Likes
from flask_login import login_required, current_user
from server_flask.db import db
import sys

# from app.utils.auth import login_required

bp = Blueprint('Admin', __name__, template_folder='templates')

@bp.route('/admin', methods=['POST', 'GET'])
@login_required
def Admin():
    if request.method == 'POST':
        task_content = request.form['content']
        task_name_post = request.form['name_post']
        new_task = Orders(client_name=client_name, city=city, warehouse=warehouse, payment_option=payment_option, phone=phone, author_id=author_id)
        #        try:
        db.session.add(new_task)
        db.session.commit()
        print(">>> Add datebase")
        return redirect('/orders')
    else:
        tasks_orders = Orders.query.order_by(Orders.timestamp).all()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        return render_template('bd/admin.html', tasks_users=tasks_users, orders=tasks_orders,  user=current_user)