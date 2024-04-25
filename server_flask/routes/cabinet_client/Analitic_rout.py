from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from black import ProductAnaliticControl
from black import an_cntrl
from black import sour_an_cntrl

prod_an_cntrl = ProductAnaliticControl()


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('Analitic', __name__, template_folder='templates')

@bp.route("/cabinet/analitic", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def analitic_test():
    if request.method == 'GET':
        all_product_analitic = prod_an_cntrl.all_product_analitic()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/product_analitic.html',
                               user=current_user, all_product_analitic=all_product_analitic)
@bp.route("/cabinet/analitic/all", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def analitic():
    if request.method == 'GET':
        items = an_cntrl.load_all()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/analitic.html',
                               user=current_user, items=items)

@bp.route('/cabinet/analitic/delete/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product(id):
    product = prod_an_cntrl.analitic_delete(id)
    print(f"Перевірка {product}")
    flash('Аналітику видалено', category='success')
    return redirect('/cabinet/analitic/all')


@bp.route('/cabinet/analitic/update_all', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_all():
    product = sour_an_cntrl.sort_analitic("all")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено ALL', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_day', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_day():
    product = sour_an_cntrl.sort_analitic("day")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено DAY', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_week', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_week():
    product = sour_an_cntrl.sort_analitic("week")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено week', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_month', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_month():
    product = sour_an_cntrl.sort_analitic("month")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено month', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_year', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_year():
    product = sour_an_cntrl.sort_analitic("year")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено week', category='success')
    return redirect('/cabinet/analitic/all')

