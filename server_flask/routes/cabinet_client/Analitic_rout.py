from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g, \
    session
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from server_flask.db import db
from black import ProductAnaliticControl
from black import AnCntrl
from black import SourAnCntrl
from black import SourDiffAnCntrl
from asx.black.analitic_cntrl.analitic_cntrl import AnaliticCntrlV2
import asyncio

import traceback
from utils import OC_logger, WorkTimeCntrl
from a_service.analitic.analitic_proc.handlers.analitic_day import CountAnaliticV2 
from a_service.analitic.base import ContextDepend

from domain.models.analitic_dto import AnaliticDto

from repository import OrderRep, AnaliticRep, ProductRep, \
    SourceRep, BalanceRepositorySQLAlchemy

from a_service.sour_an_serv import SourAnServ

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
def analitic_test_something():
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
    if request.method == 'GET':
        an_cntrl = AnCntrl()
        items = an_cntrl.load_all()
        return render_template('cabinet_client/analitic/analitic.html',
                               user=current_user, items=items)

@bp.route('/cabinet/analitic/delete/<int:id>', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def delete_product(id):
    prod_an_cntrl = AnaliticRep()
    product = prod_an_cntrl.delete_(id)
    print(f"Перевірка {product}")
    flash('Аналітику видалено', category='success')
    return redirect('/cabinet/analitic/all')


@bp.route('/cabinet/analitic/update_all', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_all():
    cntrl = AnaliticCntrlV2()
    asyncio.run(cntrl.all())
    flash('Аналітику оновлено ALL', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_day', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_day():
    try:
        cntrl = AnaliticCntrlV2()
        asyncio.run(cntrl.day())
        flash('Аналітику оновлено DAY', category='success')
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
    cntrl = AnaliticCntrlV2()
    asyncio.run(cntrl.period('week', 'day'))
    flash('Аналітику оновлено week', category='success')
    return redirect('/cabinet/analitic/all')

@bp.route('/cabinet/analitic/update_month', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_month():
    cntrl = AnaliticCntrlV2()
    asyncio.run(cntrl.period('month', 'week'))
    flash('Аналітику оновлено month', category='success')
    return redirect('/cabinet/analitic/all')
 
@bp.route('/cabinet/analitic/update_year', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_year():
    cntrl = AnaliticCntrlV2()
    asyncio.run(cntrl.period('year', 'month'))
    flash('Аналітику року оновлено', category='success')
    return redirect('/cabinet/analitic/all')
 

@bp.route('/cabinet/source/analitic_month/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_month(id):
    prod_an_cntrl = get_instance('prod_an_cntrl', ProductAnaliticControl)
    list_obj = prod_an_cntrl.load_source_difference_id_period(id, 'month')
    return render_template("cabinet_client/analitic/source_difference.html", product=list_obj, user=current_user)

@bp.route("/cabinet/analitic/day", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def analitic_test_day():
    try:
        # ctx = ContextDepend(
        #     w_time=WorkTimeCntrl(),
        #     ord_rep=OrderRep(),
        #     an_cntrl=AnCntrl(),
        #     an_rep=AnaliticRep(),
        #     logger=OC_logger.oc_log('analitic_handler'),
        #     prod_rep=ProductRep(),
        #     source_rep=SourceRep(),
        #     state=AnaliticDto,
        #     balance_rep=BalanceRepositorySQLAlchemy(db.session),
        #     source_an_cntrl=SourAnCntrl()
        # )
        # resp = CountAnaliticV2(
        #         ctx
        #     ).day()
        # print(f'{resp =}')
        cntrl = AnaliticCntrlV2()
        asyncio.run(cntrl.day())
        return 'Success Analitic' 
    except Exception as e:
        logger.error(f'analitic_day_rout: {e}')
        return 'Exception'
   

@bp.route('/analitic/edit/<int:id>', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def update_item(id):
    print(f"Перевірка ")
    rep = AnaliticRep()
    item = rep.load(id)
    flash('Редагування', category='success')
    
    return render_template('cabinet_client/analitic/edit.html',
                               user=current_user, item=item)