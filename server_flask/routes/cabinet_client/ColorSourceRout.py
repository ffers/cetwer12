from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed

from a_service.product.bot import BotProductSrv


def get_instance(class_name, class_type):
    if not hasattr(g, class_name):
        setattr(g, class_name, class_type())
    return getattr(g, class_name)


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint(
    'ColorSource', __name__,              
    template_folder='templates'
    )

@bp.route("/add_color", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def add_color():
    if request.method == 'POST':
        bot = BotProductSrv()
        resp = bot.add_color(request.form)
        if resp:
            flash("Успішно додано", "info")
            return redirect(url_for("ColorSource.add_color"))
        else:
            flash("Помилка додавання", "error")
            return redirect(url_for("ColorSource.add_color"))
    return render_template("cabinet_client/source/color_product/add_color.html", user=current_user)
    
    
