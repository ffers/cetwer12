from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify

from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from black import AnaliticControl

an_cl = AnaliticControl()

author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('Analitic', __name__, template_folder='templates')

@login_required
@admin_permission.require(http_exception=403)
@bp.route("/analitic", methods=['POST', 'GET'])
def analitic():
    if request.method == 'POST':
        analitic_product = an_cl.product_analitic_cntrl()
        print("Починаєм аналітику!")
        return render_template('cabinet_client/analitic/product_analitic.html', user=current_user, analitic_product=analitic_product)