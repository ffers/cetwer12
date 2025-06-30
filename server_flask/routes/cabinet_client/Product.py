from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import  Users
from black import ProductCntrl, ArrivelCntrl
from a_service import ProductServ
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
        return render_template('cabinet_client/product_v2/products.html',
                               user=current_user, tasks_users=tasks_users, tasks_products=tasks_products)
        
@bp.route('/cabinet/orders/get_product/changerelated', methods=['POST', 'GET'])
def Change():
    print("start")
    prod_cntrl.update_all_related()
    print("finish")
    return render_template('cabinet_client/Products/add_product.html', user=current_user)

@bp.route('/cabinet/products/add_product', methods=['POST', 'GET'])
@login_required
@manager_permission.require(http_exception=403)
def add_product():
    if request.method == 'POST':
        pr = ProductServ()
        resp = pr.add_product_v2(request.form['article'], request.form['product_name'])
        if resp:
            print(f"Product added successfully {resp}")
            if "modal" in request.form:
                responce_data = {'status': 'success', 'message': 'Product added successfully'}
                return jsonify(responce_data)
            else:
                return redirect(f'/cabinet/products/update/{resp.id}')
        else:
            print(f"!!! Product don`t added! Unsuccessfully {resp}")

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
        pr = ProductServ()
        resp = pr.update_v2(
            id,
            request.form['article'], 
            request.form['product_name']
            )
        if resp:
            flash('Продукт оновлено!', category='success')
            # return redirect(url_for('Products.Product'))
            return redirect(f'/cabinet/products/update/{id}')
        else:
            flash('Не вийшло!', category='error')
            return redirect(f'/cabinet/products/update/{id}') 
    else:
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
    try:
        if request.method == 'POST':
            if request.form.get('modal'):
                print(f"add_product_relate {request.form}")
                resp_bool = prod_cntrl.add_product_relate(request)
                print(resp_bool)
                if resp_bool:
                    return jsonify({'result': 'ok'})
                return jsonify({'result': 'false'})
            if resp_bool == True:
                flash('Компоненти додано!', category='success')
                return redirect(url_for('Products.add_product_relate'))
            else:
                flash('Компоненти недодано!', category='error')
                return redirect(url_for('Products.add_product_relate'))
        return render_template('cabinet_client/Products/add_product_relate.html', user=current_user )
    except:
        print("Працює ексепт")
        return jsonify({'result': 'false'})


@bp.route('/cabinet/products/adduse_product_relate', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def adduse_product_relate():
    try:
        if request.method == 'POST':
            if request.form.get('modal'):
                print(f"add_product_relate {request.form}")
                new_product_id = request.form.get('new_product_id')
                old_product_id = request.form.get('old_product_id')
                resp_bool = prod_cntrl.adduse_product_relate(new_product_id, old_product_id)
                print(resp_bool)
                if resp_bool:
                    return jsonify({'result': 'ok'})
                if len(resp_bool) == 0:
                    return jsonify({'result': 'product_empty'})
                return jsonify({'result': 'false'})
            if resp_bool == True:
                flash('Компоненти додано!', category='success')
                return redirect(url_for('Products.add_product_relate'))
            else:
                flash('Компоненти недодано!', category='error')
                return redirect(url_for('Products.add_product_relate'))
        return render_template('cabinet_client/Products/add_product_relate.html', user=current_user )
    except:
        print("Працює ексепт")
        return jsonify({'result': 'false'})
   
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
    return redirect(url_for(f'Products.product_relate'))


@bp.route('/cabinet/product/update_bulk', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def product_update_bulk():
    prod_cntrl = ProductCntrl()
    add = prod_cntrl.update_prod_table(request.get_json())
    if add:
        flash('Оновлено', category='success')
        return "OK", 200
    else:
        flash('Невийшло', category='error')
        return 400 
  
    
    
  




#     article = db.Column(db.String(50))
#     name = db.Column(db.String(150))
#     quantity = db.Column(db.Integer)
#     product_id = db.Column(db.Integer, db.ForeignKey(
#         'products.id', name='fk_product_relate_products_id'))
#     products = db.relatio 