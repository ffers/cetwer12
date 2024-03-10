from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from server_flask.models import  Users, Orders, Products, OrderedProduct
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed



author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('Analitic', __name__, template_folder='templates')

@login_required
@admin_permission.require(http_exception=403)
@bp.route("/analitic", methods=['POST', 'GET'])
def analitic():
    if request.method == 'POST':
        print("Починаєм аналітику!")
        return {'ok': True}
    return render_template('cabinet_client/analitic/product_analitic.html', user=current_user)