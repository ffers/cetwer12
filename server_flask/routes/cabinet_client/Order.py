import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from server_flask.models import  Users, Orders, Products, OrderedProduct
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from flask_paginate import Pagination
from server_flask.db import db
from black import tg_answ_cntrl
from helperkit.filekit import FileKit
from itertools import zip_longest
import logging, requests, json
from urllib.parse import unquote
from pytz import timezone, utc
from datetime import datetime
from black import OrderCntrl, DeliveryOrderCntrl
from utils import util_asx
from collections import Counter

OC_log = util_asx.oc_log("order")

def format_float(num_str):
    try:
        num = float(num_str)
        # Якщо число - ціле, додаємо ".00"
        if num.is_integer():
            num_dr = f"{int(num)}.00"
            return float(num_dr)
        else:
            return float(num)
    except ValueError:
        return "Неправильний формат числа"

def get_data(data, offset=0, per_page=10):
    return data[offset: offset + per_page]

ord_cntrl = OrderCntrl()
fl_cl = FileKit()

del_ord_cntrl = DeliveryOrderCntrl()
author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('Order', __name__, template_folder='templates')

@bp.route('/cabinet/orders', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def Order():
    if request.method == 'POST':
        task_content = request.form['content']
        task_name_post = request.form['name_post']
        print(">>> Add datebase")
        return redirect('/orders')
    else:
        format = "%H:%M:%S %Z%z %Y-%m-%d"
        kiyv = timezone('Europe/Kiev')
        now_utc = datetime.now(timezone('UTC'))
        print(f"Перевірка UTC {now_utc.strftime(format)}")
        kiev_now = now_utc.astimezone(timezone('Europe/Kiev'))
        # Convert to Asia/Kolkata time zone
        now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
        # now_kiyv = now_utc.astimezone(timezone(kiev))
        print(f"Перевірка {now_asia.strftime(format)}")
        print(kiev_now.strftime(format))
        tasks_orders = Orders.query.order_by(Orders.timestamp.desc()).all()
        for order in tasks_orders:
            # установити UTC
            if order.timestamp.tzinfo is None or order.timestamp.tzinfo.utcoffset(order.timestamp) is None:
                order.timestamp = order.timestamp.replace(tzinfo=utc)
            # установити Київ час
            order.timestamp = order.timestamp.astimezone(kiyv)
            # order.sum_price = "{:.2f}".format(order.sum_price)
        tasks_users = Users.query.order_by(Users.timestamp).all()
        page = request.args.get('page', default=1, type=int)
        per_page = 50

        total = len(tasks_orders)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

        offset = (page - 1) * per_page
        data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

        return render_template('cabinet_client/orders.html', pagination=pagination,
                               tasks_users=tasks_users, orders=data_subset,  user=current_user)



@bp.route('/cabinet/orders/update/<int:id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
def update(id):
    task_update = Orders.query.get_or_404(id)
    if request.method == 'POST':
        task_update.payment_method_id = request.form['payment_option']
        task_update.phone = request.form['phone']
        task_update.client_firstname = request.form['client_firstname']
        task_update.client_surname = request.form['client_surname']
        task_update.client_lastname = request.form['client_lastname']
        task_update.description = request.form['description']
        task_update.sum_before_goods = None
        if request.form['payment_option'] == "3":
            sum_before_goods_dr = request.form["sum_before_goods"]
            sum_before_goods = format_float(sum_before_goods_dr)
            task_update.sum_before_goods = sum_before_goods
        if "city" in request.form:
            task_update.warehouse_option = request.form['warehouse_option']
            task_update.city_ref = request.form['CityREF']
            task_update.city_name = request.form['CityName']
            task_update.warehouse_ref = request.form['warehouse-id']
            task_update.warehouse_text = unquote(request.form['warehouse-text'])
        if "product" in request.form:
            sum_price_draft = request.form['total-all']
            task_update.sum_price = format_float(sum_price_draft)
            task_update.description = request.form['description']
            task_update.sum_after_goods = None
            task_update.ordered_product = []
            product_id = request.form.getlist('product')
            price = request.form.getlist('price')
            quantity = request.form.getlist('quantity')
            print(f"data {product_id} & {price} & {quantity}")
            combined_list = list(zip_longest(product_id, price, quantity, fillvalue=None))
            for item in combined_list:
                product_id, price, quantity = item
                ordered_product = OrderedProduct(product_id=product_id, price=price, quantity=quantity, order_id=task_update.id)
                task_update.ordered_product.append(ordered_product)
        db.session.commit()
        print(">>> Update in datebase")
        flash(f'Замовлення {task_update.id} оновлено', category='success')
        return redirect('/cabinet/orders')
        # except:
        #     return 'There was an issue updating your task'

    else:
        print(f"перевірка {vars(current_user.roles)}")
        return render_template('cabinet_client/update_order.html', order=task_update, user=current_user)

@bp.route('/cabinet/orders/add_order', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def add_order():
    if request.method == 'POST':
        sum_price_draft = request.form["total-all"]
        sum_before_goods = None
        if request.form['payment_option'] == "3":
            sum_before_goods = request.form["sum_before_goods"]
        print(f"ПРИНТУЄМ !!!! ")
        order = Orders(description=request.form['description'], city_name=request.form['CityName'], city_ref=request.form['CityREF'],
                      warehouse_text=unquote(request.form['warehouse-text']), warehouse_ref=request.form['warehouse-id'],
                       phone=request.form['phone'], author_id=current_user.id, client_firstname=request.form['client_firstname'],
                       client_lastname=request.form['client_lastname'], client_surname=request.form['client_surname'],
                       warehouse_option=request.form['warehouse_option'], delivery_option="nova_poshta",
                       payment_method_id=request.form['payment_option'], sum_price=format_float(sum_price_draft),
                       sum_before_goods=sum_before_goods, delivery_method_id=1, source_order_id=1, ordered_status_id=10,
                       description_delivery="Одяг Jemis")
        db.session.add(order)
        db.session.commit()
        ord_cntrl.add_order_code(order)
        product_id = request.form.getlist('product')
        price = request.form.getlist('price')
        quantity = request.form.getlist('quantity')
        print(f"data {product_id} & {price} & {quantity}")
        combined_list = list(zip_longest(product_id, price, quantity, fillvalue=None))
        for item in combined_list:
            data = OrderedProduct(product_id=item[0], price=item[1], quantity=item[2], order_id=order.id)
            db.session.add(data)
        db.session.commit()
        flash('Замовлення створено', category='success')
        return redirect(url_for('Order.Order'))

    return render_template('cabinet_client/add_order.html', user=current_user)



@bp.route('/cabinet/orders/confirmed/<int:id>', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def send_cab(id):
    if request.method == 'POST':
        return redirect('/cabinet/orders')
    else:
        print(f"Працює {id}")
        resp = ord_cntrl.confirmed_order(id, 2)
        if resp["success"] == True:
            flash('Замовлення НП створено', category='success')
        else:
            flash('Замовлення НП нестворено', category='error')
        return redirect('/cabinet/orders')

@bp.route('/cabinet/orders/get_cities', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def get_cities():
    try:
        search_query = request.args.get('q', '').lower()
        count = 0
        for item in search_query:
            count += 1
        if count > 3:
            # print(count)
            cities_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")
            print(f"warehouse_option {request.args}")
            # Фільтрація даних за текстовим запитом
            filtered_data = [item for item in cities_data["City"] if search_query in item["City"].lower()]
            if filtered_data:  # print(f"данні отриманні {filtered_data}")
                return jsonify({'results': filtered_data})
            else:
                 return jsonify({'results': []})
        else:
            return jsonify({'results': []})
    except Exception as e:
        OC_log.info("Помилка пошуку міста %s", e)
        return jsonify({'results': []})



@bp.route('/cabinet/orders/get_warehouse', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def get_warehouse():
    city_ref = request.args.get('cityRef')
    print(f"отриманий реф міста {city_ref}")
    # warehouse_option = request.form['warehouse_option']
    print(f"warehouse_option {request.args}")
    search_query = request.args.get('q', '').lower()
    cities_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")

    # Фільтрація даних за текстовим запитом
    city_data = next((item for item in cities_data["City"] if city_ref in item["CityRef"].lower()), None)
    # print(f"дивимось {city_data}")
    if city_data:
        # Здійснити пошук відділень в даному місті
        warehouse_data = [warehouse for warehouse in city_data['Warehouse'] if search_query in warehouse['Description'].lower()]
        print(f"дивимось відділеня  {warehouse_data}")
        return jsonify({'results': warehouse_data})
    else:
        return jsonify({'results': []})

@bp.route('/cabinet/orders/get_post', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def get_post():
    city_ref = request.args.get('cityRef')
    print(f"warehouse_option {request.args}")
    print(f"отриманий реф міста {city_ref}")

    search_query = request.args.get('q', '').lower()
    cities_data = fl_cl.directory_load_json("api/nova_poshta/create_data/warehouses")

    # Фільтрація даних за текстовим запитом
    city_data = next((item for item in cities_data["City"] if city_ref in item["CityRef"].lower()), None)

    # print(f"дивимось {city_data}")
    if city_data:
        # Здійснити пошук відділень в даному місті
        warehouse_data = [warehouse for warehouse in city_data['Post'] if search_query in warehouse['Description'].lower()]
        print(f"дивимось поштомат  {warehouse_data}")
        return jsonify({'results': warehouse_data})
    else:
        return jsonify({'results': []})

@bp.route('/cabinet/orders/get_product', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def get_product():
    search_query = request.args.get('q', '').lower()
    tasks_products = Products.query.order_by(Products.timestamp).all()
    products_list = []
    for prod in tasks_products:
        prod_data = {
            'id': prod.id,
            'article': prod.article + ' - ' + prod.product_name
        }
        products_list.append(prod_data)
    print(products_list)
    if products_list:
        # Здійснити пошук відділень в даному місті
        result = [warehouse for warehouse in products_list if search_query in warehouse['article'].lower()]
        print(f"дивимось продукти  {result}")
        return jsonify({'results': result})
    else:
        return jsonify({'results': []})





# @bp.route('/cabinet/orders/get_product/send_with_prom_test', methods=['GET'])
# def get_prom_to_crm_test():
#     data = json.dumps(data_order)
#     headers = {'Content-Type': 'application/json'}
#     url = 'http://localhost:5000/cabinet/orders/get_product/send_with_promd6a9aeb0071216fb3d482707a0b79d401a8ef1dd'
#     resp = requests.post(url, data=data, headers=headers)
#     print(resp.text)  # виведе відповідь від сервера
#     return jsonify({"results": "success"})

@bp.route('/cabinet/orders/get_product/send_with_prom', methods=['POST'])
def get_prom_to_crm():
    token = request.headers.get("Authorization")
    json_data = request.json
    if verify_token(token):
        if json_data:
            resp = ord_cntrl.add_order(json_data)
            return jsonify({'results': 'success', 'order_id': resp})
        else:
            return jsonify({'results': []})
    else:
        return jsonify({'result': 'forbiden'}), 401

@bp.route('/cabinet/orders/get_product/update_with_prom', methods=['POST'])
def get_update_order():
    token = request.headers.get("Authorization")
    json_data = request.json
    print("Отримали запит від scrypt")
    if verify_token(token):
        if json_data:
            resp = tg_answ_cntrl.await_order(json_data, "update_to_crm")
            return jsonify({'results': 'success', 'order_id': resp})
        else:
            return jsonify({'results': "Don`t have body"})
    else:
        return jsonify({'result': 'forbiden'}), 401

def verify_token(token):
    valid_token = os.getenv("SEND_TO_CRM_TOKEN")
    if token == valid_token:
        return True
    return False



@bp.route('/cabinet/orders/delete/<int:id>')
@login_required
@admin_permission.require(http_exception=403)
def delete(id):
    try:
        task_to_delete = ord_cntrl.delete_order(id)
        flash(f'Замовлення видалено', category='success')
        return redirect('/cabinet/orders')
    except:
        return 'Це замовлення вже було видаленно'


@bp.route('/cabinet/orders/dublicate/<int:id>', methods=['GET', 'POST'])
@login_required
@author_permission.require(http_exception=403)
def dublicate(id):
    ord_cntrl.dublicate(id)
    return redirect('/cabinet/orders')


@bp.route('/cabinet/orders/search_for_phone', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def search_for_phone():
    search = ord_cntrl.search_for_phone(request)
    return search

@bp.route('/cabinet/order_draft', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def order_draft():
    if request.method == 'POST':
        print(">>> Add datebase")
        print(f"order_draft {request.json}")
        bool = del_ord_cntrl.add_registr(request.json)
        if bool:
            print(f"bool {bool}")
            # flash(f'ТТН додано до реєстр', category='success')
        else:
            flash(f'Невийшло', category='error')
        return jsonify(bool)
    else:
        tasks_orders = ord_cntrl.load_confirmed_order()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        page = request.args.get('page', default=1, type=int)
        per_page = 50
        total = len(tasks_orders)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
        offset = (page - 1) * per_page
        data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

        return render_template('cabinet_client/order_draft.html', pagination=pagination,
                               tasks_users=tasks_users, orders=data_subset,  user=current_user)

@bp.route('/cabinet/orders/del_reg', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def reg():
    print(">>> Delete reg datebase")
    print(f"order_draft {request.json}")
    bool = del_ord_cntrl.delete_ttn_in_reg(request.json)
    # del_ord_cntrl.add_registr(request.form.getlist('selectedItems'))
    if bool:
        # flash(f'Видалено з реєстру', category='success')
        return jsonify({"succes": True})
    else:
        # flash(f'Невийшло', category='error')
        return jsonify({"succes": False})

@bp.route('/cabinet/orders/changeStatus', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def changeStatus():
    print(">>> Change status")
    print(f"order_draft {request.json}")
    bool = ord_cntrl.change_status(request.json)
    if bool:
        # flash(f'Змінено статус', category='success')
        return jsonify({"succes": True})
    else:
        # flash(f'Невийшло', category='error')
        return jsonify({"succes": False})

@bp.route('/cabinet/orders/filter/confirmeded', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def confirmeded():
    tasks_orders = ord_cntrl.load_confirmed_order()
    tasks_users = Users.query.order_by(Users.timestamp).all()
    page = request.args.get('page', default=1, type=int)
    per_page = 50
    total = len(tasks_orders)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    offset = (page - 1) * per_page
    data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

    return render_template('cabinet_client/order_draft.html', pagination=pagination,
                           tasks_users=tasks_users, orders=data_subset, user=current_user)

@bp.route('/cabinet/orders/filter/registered', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def registered():
    tasks_orders = ord_cntrl.load_registred()
    tasks_users = Users.query.order_by(Users.timestamp).all()
    page = request.args.get('page', default=1, type=int)
    per_page = 50
    total = len(tasks_orders)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    offset = (page - 1) * per_page
    data_subset = get_data(tasks_orders, offset=offset, per_page=per_page)

    return render_template('cabinet_client/order_draft.html', pagination=pagination,
                           tasks_users=tasks_users, orders=data_subset, user=current_user)




#  id |        name        | description
# ----+--------------------+-------------
#   1 | Підтвердити        |
#   2 | Підтвержено        |
#   3 | Оплачено           |
#   4 | Несплачено         |
#   5 | Скасовано          |
#   6 | Предзамовлення     |
#   7 | Питання            |
#   8 | Відправлено        |
#   9 | Отримано           |
#  10 | Нове               |
#  11 | Очікує відправленя |
#  12 | Виконано           |
#  13 | Тест               |

#  id | name |                               description                               | code
# ----+------+-------------------------------------------------------------------------+------
#   1 |      | Відправник самостійно створив цю накладну, але ще не надав до відправки |    1
#   2 |      | Видалено                                                                |    2
#   3 |      | Прибув на відділення                                                    |    7
#   4 |      | Відправлення отримано                                                   |    9
#   5 |      | На шляху до одержувача                                                  |  101
#   6 |      | Відмова одержувача (отримувач відмовився від відправлення)              |  103
# https://api.telegram.org/bot603175634:AAHNHBKy56g37S1WiS1KZuw_a-aZjahqD7o/getFile?file_id=AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ