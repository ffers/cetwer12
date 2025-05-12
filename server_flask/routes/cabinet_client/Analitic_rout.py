from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g, \
    session
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from black import ProductAnaliticControl
from black import AnCntrl
from black import SourAnCntrl
from black import SourDiffAnCntrl
import traceback
from utils import OC_logger

def get_instance(class_name, class_type):
    if not hasattr(g, class_name):
        setattr(g, class_name, class_type())
    return getattr(g, class_name)

logger = OC_logger.oc_log('analitic_rout')


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('Analitic', __name__, template_folder='templates')

@bp.route("/cabinet/analitic", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def analitic_test():
    if request.method == 'GET':
        prod_an_cntrl = get_instance('prod_an_cntrl', ProductAnaliticControl)
        all_product_analitic = prod_an_cntrl.all_product_analitic()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/product_analitic.html',
                               user=current_user, all_product_analitic=all_product_analitic)
    
@bp.route("/cabinet/analitic/all", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def analitic():
    print(session)
    if request.method == 'GET':
        an_cntrl = AnCntrl()
        items = an_cntrl.load_all()
        return render_template('cabinet_client/analitic/analitic.html',
                               user=current_user, items=items)

@bp.route('/cabinet/analitic/delete/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product(id):
    prod_an_cntrl = get_instance('prod_an_cntrl', ProductAnaliticControl)
    product = prod_an_cntrl.analitic_delete(id)
    print(f"Перевірка {product}")
    flash('Аналітику видалено', category='success')
    return redirect('/cabinet/analitic/all')


@bp.route('/cabinet/analitic/update_all', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_all():
    sour_an_cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    product = sour_an_cntrl.update_all_analitic()
    print(f"Перевірка {product}")
    flash('Аналітику оновлено ALL', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_day', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_day():
    try:
        sour_an_cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
        product = sour_an_cntrl.sort_analitic("day")
        print(f"Перевірка {product}")
        flash('Аналітику оновлено DAY', category='success')
        session.update({'test': 'test'})
        print(session)
        return redirect('/cabinet/analitic/all')
    except Exception as e:
        print('Помилка')
        logger.exception(f'update_day:')
        flash('Аналітику неоновлено', category='error')
        return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_week', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_week():
    sour_an_cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    product = sour_an_cntrl.sort_analitic("week")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено week', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_month', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_month():
    sour_an_cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    product = sour_an_cntrl.sort_analitic("month")
    print(f"Перевірка {product}")
    flash('Аналітику оновлено month', category='success')
    return redirect('/cabinet/analitic/all')
 
@bp.route('/cabinet/analitic/update_year', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_year():
    sour_an_cntrl = get_instance('sour_an_cntrl', SourAnCntrl)
    product = sour_an_cntrl.sort_analitic("year")
    print(f"Перевірка {product}")
    flash('Аналітику року оновлено', category='success')
    return redirect('/cabinet/analitic/all')
 

@bp.route('/cabinet/source/analitic_month/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_month(id):
    prod_an_cntrl = get_instance('prod_an_cntrl', ProductAnaliticControl)
    list_obj = prod_an_cntrl.load_source_difference_id_period(id, 'month')
    return render_template("cabinet_client/analitic/source_difference.html", product=list_obj, user=current_user)
   