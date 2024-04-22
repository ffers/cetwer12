from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import  Users
from decimal import Decimal
from repository import sour_an_rep as rep
from black import sour_an_cntrl as cntrl

manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('ProductSource', __name__, template_folder='templates')

@bp.route('/cabinet/source/get_source', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_source():
    search_query = request.args.get('q', '').lower()
    items = rep.load_all()
    result = []
    for item in items:
        if search_query in item.article.lower():
            prod_data = {
                'id': item.article,
                'article': item.article + ' - ' + item.name
            }
            result.append(prod_data)
    print(f"дивимось продукти  {result}")
    if result:
        return jsonify({'results': result})
    else:
        return jsonify({'results': []})


@bp.route('/cabinet/products/add_source', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_source():
    if request.method == 'POST':
        print("ПРацюєм")
        resp_bool = cntrl.add_source(request)
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            responce_data = {'status': 'success', 'message': 'Product relate added successfully'}
            flash('Продукт створено!', category='success')
            return redirect(url_for('Products.product_source'))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('Products.add_product_relate'))
    return render_template('cabinet_client/Products/add_product_source.html', user=current_user )

@bp.route('/cabinet/source/add_arrival', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_arrival():
    if request.method == 'POST':
        print("ПРацюєм")
        resp_bool = cntrl.add_arrival(request)
        for item in request.form:
            print(item)
        if resp_bool == True:
            print("Product added successfully")
            responce_data = {'status': 'success', 'message': 'Product relate added successfully'}
            flash('Продукт створено!', category='success')
            return redirect(url_for('Products.product_source'))
        else:
            print(request.form)
            print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return redirect(url_for('Products.add_product_relate'))
    return render_template('cabinet_client/Products/add_product_source.html', user=current_user)
