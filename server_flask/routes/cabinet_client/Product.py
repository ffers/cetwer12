from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed, Principal
from flask_login import login_required, current_user
from server_flask.db import db
from server_flask.models import  Users, Products, Orders

manager = RoleNeed('manager')
author_permission = Permission(manager)
bp = Blueprint('Products', __name__, template_folder='templates')

def format_float(num_str):
    try:
        num = float(num_str)
        # Якщо число - ціле, додаємо ".00"
        if num.is_integer():
            return f"{int(num)}.00"
        else:
            return float(num)
    except ValueError:
        return None

@bp.route('/cabinet/products', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def Product():
    if request.method == 'POST':
        return redirect('/products')
    else:
        tasks_products = Products.query.order_by(Products.timestamp).all()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        return render_template('cabinet_client/Products/products.html',
                               user=current_user, tasks_users=tasks_users, tasks_products=tasks_products)

@bp.route('/cabinet/products/add_product', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def add_product():
    if request.method == 'POST':
        article = request.form['article']
        product_name = request.form['product_name']
        description = request.form['description']
        input_value = request.form['quantity']
        if input_value:
            quantity = int(input_value)
        else:
            quantity = None
        price_ch = request.form['price']
        print(price_ch)
        price = format_float(price_ch)
        print(price, product_name)
        post = Products(description=description, article=article,
                      product_name=product_name,
                      price=price, quantity=quantity)
        db.session.add(post)
        db.session.commit()

        order = Orders.query.order_by(Orders.id.desc()).first()
        if "modal" in request.form:
            responce_data = {'status': 'success', 'message': 'Product added successfully'}
            print(responce_data)
            return jsonify(responce_data)
        else:
            flash('Продукт створено!', category='success')
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('Products.Product'))

    return render_template('cabinet_client/Products/add_product.html', user=current_user )

@bp.route('/cabinet/products/count', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def call_product():
    return redirect(url_for('Products.Product'))
