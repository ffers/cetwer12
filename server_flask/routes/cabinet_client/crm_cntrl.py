from repository.crm_sqlalchemy import CrmRepositorySQLAlchemy
from a_service.crm_service import CrmService

from flask import Blueprint, render_template, request, redirect, url_for, \
    jsonify
from server_flask.db import db
from flask_login import login_required, current_user

from flask_principal import Permission, RoleNeed

admin = RoleNeed('admin')
admin_permission = Permission(admin)

author = RoleNeed('manager')
author_permission = Permission(author)

bp = Blueprint('crm', __name__)

repo = CrmRepositorySQLAlchemy(db.session)
service = CrmService(repo)

temp = 'cabinet_client/crm/'

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
    if request.method == 'POST':
        service.create_item(
            request.form['name'],
            current_user.id
            )
        return redirect(url_for('crm.index'))
    return render_template(f'{temp}create.html', user=current_user) 

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = service.get_item(item_id)
    if request.method == 'POST':
        service.update_item(
            item.id, 
            request.form['name']
            )
        return redirect(url_for('crm.index'))
    return render_template(f'{temp}edit.html', item=item, user=current_user)

@login_required
@admin_permission.require(http_exception=403)
@bp.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    service.delete_item(item_id)
    return redirect(url_for('crm.index'))


@bp.route('/list_select', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def list_select():
    items = service.get_items_select()
    if items:
        return jsonify({'results': items})
    else:
        return jsonify({'results': []})
