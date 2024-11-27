from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from flask_paginate import Pagination

from black import jour_ch_cntrl as journal
from black import sour_an_cntrl


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('JournalChange', __name__, template_folder='templates')

def get_data(data, offset=0, per_page=10):
    return data[offset: offset + per_page]

@bp.route("/cabinet/journal/all", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def load_all():
    if request.method == 'GET':
        items = journal.load_all() 
        page = request.args.get('page', default=1, type=int)
        per_page = 150

        total = len(items)
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')

        offset = (page - 1) * per_page
        data_subset = get_data(items, offset=offset, per_page=per_page)
        return render_template('cabinet_client/analitic/journal_change.html', pagination=pagination,
                               user=current_user, items=data_subset)
    

@bp.route("/cabinet/journal_ch/day_analitic", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def day_analitic():
    if request.method == 'GET':
        data = d_an_cntrl.main()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/day_analitic.html',
                               user=current_user, data=data)

@bp.route('/cabinet/journal_ch/delete/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product(id):
    product = prod_an_cntrl.analitic_delete(id)
    print(f"Перевірка {product}")
    flash('Аналітику видалено', category='success')
    return redirect('/cabinet/analitic')


