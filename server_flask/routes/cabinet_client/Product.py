from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import  Users
from black import ProductCntrl, ArrivelCntrl
from decimal import Decimal

arriv_cntrl = ArrivelCntrl()
prod_cntrl = ProductCntrl()
manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('Products', __name__, template_folder='templates')


def format_float(num):
    try:
        if isinstance(num, int):
            num_format = str(f"{int(num)}.00")
            # Конвертуємо int у Decimal
            return Decimal(num_format)
        else:
            num_format = float(num)
            # Конвертуємо float у Decimal
            return Decimal(str(f"{num_format: .2f}"))
    except ValueError:
        return None

@bp.route('/cabinet/products', methods=['POST', 'GET'])
@login_required
@manager_permission.require(http_exception=403)
def Product():
    if request.method == 'POST':
        return redirect('/products')
    else:
        tasks_products = prod_cntrl.load_product_all()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        return render_template('cabinet_client/Products/products.html',
                               user=current_user, tasks_users=tasks_users, tasks_products=tasks_products)

@bp.route('/cabinet/products/add_product', methods=['POST', 'GET'])
@login_required
@manager_permission.require(http_exception=403)
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
        resp_bool = prod_cntrl.add_product(description, article, product_name, price, quantity)
        if resp_bool == True:
            print("Product added successfully")
            if "modal" in request.form:
                responce_data = {'status': 'success', 'message': 'Product added successfully'}
                print(responce_data)
                flash('Продукт створено!', category='success')
                return jsonify(responce_data)
            else:
                print(request.form)
                print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return redirect(url_for('Products.Product'))
        else:
            print("!!! Product don`t added! Unsuccessfully")

    return render_template('cabinet_client/Products/add_product.html', user=current_user )

@bp.route('/cabinet/products/count', methods=['POST', 'GET'])
@login_required
@manager_permission.require(http_exception=403)
def call_product():
    return redirect(url_for('Products.Product'))


@bp.route('/cabinet/products/update/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def update(id):
    product = prod_cntrl.load_product_item(id)
    if request.method == 'POST':
        resp = prod_cntrl.update_product(request, id)
        if resp == True:
            flash('Продукт оновлено!', category='success')
            # return redirect(url_for('Products.Product'))
            return render_template(
                'cabinet_client/Products/update_product.html',
                user=current_user, product=product)

        else:
            flash('Не вийшло!', category='warning')
            return redirect(url_for('Products.Product'))
    else:
        product = prod_cntrl.load_product_item(id)
        print(f"Перевірка {product}")
        return render_template(
            'cabinet_client/Products/update_product.html',
            user=current_user, product=product)

@bp.route('/cabinet/products/delete/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product(id):
    product = prod_cntrl.delete_product(id)
    print(f"Перевірка {product}")
    flash('Продукт видалено', category='success')
    return render_template(
        'cabinet_client/Products/products.html',
        user=current_user, product=product)

# @bp.route('/cabinet/orders/fd', methods=['POST', 'GET'])
# def body_price():
#     prod_cntrl.changeBodyPrice()
#     return jsonify({"success": True})
#

@bp.route('/cabinet/products/add_product_relate', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_product_relate():
    if request.method == 'POST':
        print("ПРацюєм")
        resp_bool = prod_cntrl.add_product_relate(request)
        print(resp_bool)
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            responce_data = {'status': 'success', 'message': 'Product relate added successfully'}
            flash('Продукт створено!', category='success')
            return redirect(url_for('Products.product_relate'))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('Products.add_product_relate'))
    return render_template('cabinet_client/Products/add_product_relate.html', user=current_user )

@bp.route('/cabinet/products/update_product_relate/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_product_relate(id):
    item = prod_cntrl.load_product_relate_item(id)
    if request.method == 'POST':
        resp_bool = prod_cntrl.update_prod_relate(id, request)
        resp_bool = True
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            flash('Продукт оновлено!', category='success')
            return redirect(url_for(f'Products.product_relate'))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for(f'Products.product_source'))
    return render_template('cabinet_client/Products/update_product_relate.html',
                           user=current_user, item=item )


@bp.route('/cabinet/products/product_relate', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def product_relate():
    items = prod_cntrl.load_product_relate()
    return render_template('cabinet_client/Products/product_relate.html',
                           user=current_user, items=items)

@bp.route('/cabinet/products/delete_relate/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product_relate(id):
    product = prod_cntrl.delete_product_relate(id)
    print(f"Перевірка {product}")
    flash('Продукт видалено', category='success')
    return render_template(
        'cabinet_client/Products/product_relate.html',
        user=current_user, product=product)








#     article = db.Column(db.String(50))
#     name = db.Column(db.String(150))
#     quantity = db.Column(db.Integer)
#     product_id = db.Column(db.Integer, db.ForeignKey(
#         'products.id', name='fk_product_relate_products_id'))
#     products = db.relatio