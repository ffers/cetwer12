from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from a_service import PanelSetServ

manager = RoleNeed('admin')
author_permission = Permission(manager)
bp = Blueprint('Panel', __name__, template_folder='templates')



@bp.route('/payment_method', methods=['POST', 'GET'])
@login_required
@author_permission.require(http_exception=403)
def payment_method():
    if request.method == 'POST':
        print(">>> Add datebase")
        return redirect('/orders')
    else:
        items = PanelSetServ().load_all()
        return render_template('cabinet_client/work_space/payment_method.html', items=items,  user=current_user)
