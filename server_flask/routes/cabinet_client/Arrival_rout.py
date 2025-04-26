from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import Users
from black import ArrivelCntrl, SourAnCntrl


arriv_cntrl = ArrivelCntrl() 
manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('Arrival', __name__, template_folder='templates')

# @bp.route('/cabinet/arrival/add_arrival', methods=['POST', 'GET'])
# @login_required
# @admin_permission.require(http_exception=403)
# def add_arrival():
#     if request.method == 'POST':
#         print("ПРацюєм")
#         cntrl = SourAnCntrl()
#         resp_bool = cntrl.add_arrival(request)
#         print(resp_bool, "resp_bool")
#         for item in request.form:
#             print(item)
#         if resp_bool == True:
#             print("Product added successfully")
#             responce_data = {'status': 'success', 'message': 'Product relate added successfully'}
#             flash('Поставлено на прихід!', category='success')
#             return redirect("add_arrival")
#         else:
#             print(request.form)
#             print("НЕВИЙШЛО!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             flash('Не вийшло!', category='success')
#             return redirect("add_arrival")
#     return render_template('cabinet_client/source/source/add_arrival.html', user=current_user ) 


# @bp.route('/cabinet/products/arrival_list', methods=['POST', 'GET'])
# @login_required
# @admin_permission.require(http_exception=403)
# def arrival_list():
#     arrival = arriv_cntrl.load_all_arrival()
#     return render_template('cabinet_client/source/source/arrival_list.html', user=current_user, arrival=arrival)
