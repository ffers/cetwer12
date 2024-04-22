from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_principal import Permission, RoleNeed
from flask_login import login_required, current_user
from server_flask.models import  Users
from decimal import Decimal
from repository import sour_an_rep as rep

manager = RoleNeed('manager')
manager_permission = Permission(manager)
admin_permission = Permission(RoleNeed('admin'))
bp = Blueprint('ProductSource', __name__, template_folder='templates')

@bp.route('/cabinet/source/get_source', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_source():
    search_query = request.args.get('q', '').lower()
    items = rep.load_all()
    result = []
    for item in items:
        if search_query in item.article.lower():
            prod_data = {
                'id': item.article,
                'article': item.article + ' - ' + item.name
            }
            result.append(prod_data)
    print(f"дивимось продукти  {result}")
    if result:
        return jsonify({'results': result})
    else:
        return jsonify({'results': []})