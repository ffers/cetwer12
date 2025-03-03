from flask import Blueprint, render_template, request, g
from flask import flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from pydantic import RedisDsn
from server_flask.models import  Users
from decimal import Decimal
from repository import sour_an_rep as rep
from black import SourAnCntrl

manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('ProductSource', __name__, template_folder='templates')


def get_instance(class_name, class_type):
    if not hasattr(g, class_name):
        setattr(g, class_name, class_type())
    return getattr(g, class_name)


@bp.route('/cabinet/source/get_source', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_source():
    cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    result = cntrl.get_search(request)
    if result:
        return jsonify({'results': result})
    else:
        return jsonify({'results': []})


@bp.route('/cabinet/source/add', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403) 
def add():
    if request.method == 'POST':
        print("ПРацюєм")
        cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
        resp_bool = cntrl.add(request)
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            responce_data = {'status': 'success', 'message': 'Product relate added successfully'}
            flash('Додано джерело!', category='success')
            return redirect(url_for(f"ProductSource.add"))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('Products.add_product_relate'))
    return render_template('cabinet_client/Products/add_product_source.html', user=current_user )



@bp.route('/cabinet/source/update/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def update(id):
    cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    item = cntrl.load_item(id)
    if request.method == 'POST':
        cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
        resp_bool = cntrl.update(id, request)
        resp_bool = True
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            flash('Продукт оновлено!', category='success')
            return redirect(url_for(f'ProductSource.all'))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for(f'ProductSource.all'))
    return render_template('cabinet_client/Products/update_product_source.html',
                           user=current_user, item=item )

@bp.route('/cabinet/source/all', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def all():
    cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    items = cntrl.load_all()
    money = 0
    for item in items:
        money = item.money + money
    return render_template('cabinet_client/Products/product_source.html',
                           user=current_user, items=items, money=money)

@bp.route('/cabinet/source/delete/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product_source(id):
    cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    product = cntrl.delete(id)
    print(f"Перевірка {product}")
    flash('Продукт видалено', category='success')
    return redirect(url_for(f'ProductSource.all'))