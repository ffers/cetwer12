from repository.balance_sqlalchemy import BalanceRepositorySQLAlchemy
from asx.a_service.analitic.balance_serv.balance_service import BalanceService
from black.analitic_cntrl.balance_cntrl import BalanceCntrl
from domain.models.move_balance_dto import MoveBalanceDTO
from utils.format_float import format_float

from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify
from server_flask.db import db
from flask_login import login_required, current_user

from flask_principal import Permission, RoleNeed

from utils import OC_logger

import os

logger = OC_logger.oc_log('balance_cntrl')

admin = RoleNeed('admin')
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('balance', __name__)

repo = BalanceRepositorySQLAlchemy(db.session)
service = BalanceService(repo)
cntrl = BalanceCntrl(repo)

temp = 'cabinet_client/balance/'
'''
PATH - balance/
'''

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/')
def index():
    items = service.list_items()
    return render_template(f'{temp}list.html', items=items, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/create', methods=['GET', 'POST'])
def create():
    try:
        if request.method == 'POST':
            service.create_item(
                request.form['balance'],
                request.form['wait'],
                request.form['stock'],
                request.form['inwork']
                )
            return redirect(url_for('balance.index'))
        return render_template(f'{temp}create.html', user=current_user) 
    except Exception as e:
        logger.exception(f'create: {e}')
        return 'Exception'

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = service.get_item(item_id)
    if request.method == 'POST':
        service.update_item(
            item.id, 
            request.form['balance'],
            request.form['wait'],
            request.form['stock'],
            request.form['inwork']
            )
        return redirect(url_for('balance.index'))
    return render_template(f'{temp}edit.html', item=item, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    service.delete_item(item_id)
    return redirect(url_for('balance.index'))


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def list_select():
    items = service.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})


@login_required
@admin_permission.require(http_exception=403)
@bp.route('/income', methods=['POST', 'GET'])
def move_balance():
    try:
        if request.method == 'POST':
            project_id = int(os.getenv('PROJECT_ID'))
            move_dto = MoveBalanceDTO(
                project_id,
                format_float(request.form['sum']),
                request.form['description'],
            )
            print(move_dto)
            item = cntrl.move_balance(move_dto)
            return render_template(f'{temp}move_balance.html', user=current_user)
        else: 
            return render_template(f'{temp}move_balance.html', user=current_user)

    except Exception as e:
        print(f"move_balance помилка {e}")
        return "Помилка"
    

    '''
    временная функция с конкретним айди проекта
    '''
@login_required
@admin_permission.require(http_exception=403)
@bp.route('/project', methods=['GET'])
def project():
    try:
        item = service.get_item(2) 
        return render_template(f'{temp}project.html', item=item, user=current_user)
    except Exception as e:
        print(f"income_balance помилка {e}")
        return "Помилка"