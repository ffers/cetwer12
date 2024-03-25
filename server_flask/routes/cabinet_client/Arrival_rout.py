from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import Users
from black import ArrivelCntrl


arriv_cntrl = ArrivelCntrl()
manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('Arrival', __name__, template_folder='templates')

@bp.route('/cabinet/products/add_arrival', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_arrival():
    if request.method == 'POST':
        resp = arriv_cntrl.add_arrival(request)
    return render_template('cabinet_client/Products/add_arrival.html', user=current_user )


@bp.route('/cabinet/products/arrival_list', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def arrival_list():
    arrival = arriv_cntrl.load_all_arrival()
    return render_template('cabinet_client/Products/arrival_list.html', user=current_user, arrival=arrival)
