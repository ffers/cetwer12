from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from black import ProductAnaliticControl
from black import DayAnalitic

prod_an_cntrl = ProductAnaliticControl()
d_an_cntrl = DayAnalitic()

author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('Analitic', __name__, template_folder='templates')

@login_required
@admin_permission.require(http_exception=403)
@bp.route("/cabinet/analitic", methods=['POST', 'GET'])
def analitic():
    if request.method == 'GET':
        all_product_analitic = prod_an_cntrl.all_product_analitic()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/product_analitic.html',
                               user=current_user, all_product_analitic=all_product_analitic)

@login_required
@admin_permission.require(http_exception=403)
@bp.route("/cabinet/day_analitic", methods=['POST', 'GET'])
def day_analitic():
    if request.method == 'GET':
        data = d_an_cntrl.main()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/day_analitic.html',
                               user=current_user, data=data)


@login_required
@admin_permission.require(http_exception=403)
@bp.route('/cabinet/analitic/delete/<int:id>', methods=['GET'])
def delete_product(id):
    product = prod_an_cntrl.analitic_delete(id)
    print(f"Перевірка {product}")
    flash('Аналітику видалено', category='success')
    return redirect('/cabinet/analitic')