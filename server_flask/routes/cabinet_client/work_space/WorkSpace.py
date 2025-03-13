from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from a_service import WorkSpaceServ

admin = RoleNeed('admin')
admin_permission = Permission(admin)
bp = Blueprint('Panel', __name__, template_folder='templates')



@bp.route('/payment_method', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def payment_method():
    if request.method == 'POST':
        return redirect('/orders')
    else:
        items = WorkSpaceServ().load_payment_methods()
        return render_template('cabinet_client/work_space/payment_method.html', items=items,  user=current_user)
    
@bp.route('/delivery_method', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def delivery_method():
    if request.method == 'POST':
        return redirect('/orders')
    else:
        items = WorkSpaceServ().load_delivery_methods()
        return render_template('cabinet_client/work_space/delivery_method.html', items=items,  user=current_user)

@bp.route('/sources_order', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def source_order():
    if request.method == 'POST':
        return redirect('/orders')
    else:
        items = WorkSpaceServ().load_sources_order()
        return render_template(
            'cabinet_client/work_space/sources_order.html', 
            items=items,  
            user=current_user
            )
    
@bp.route('/work_space_choice', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def work_space_choice():
    if request.method == 'POST':
        return redirect('/orders')
    else:
        items = WorkSpaceServ().load_sources_order()
        return render_template(
            'cabinet_client/work_space/work_space.html', 
            items=items,  
            user=current_user
            )
