from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, g
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from black import SourDiffAnCntrl

def get_instance(class_name, class_type):
    if not hasattr(g, class_name):
        setattr(g, class_name, class_type())
    return getattr(g, class_name)


author_permission = Permission(RoleNeed('manager'))
admin_permission = Permission(RoleNeed('admin'))

bp = Blueprint('SourceDifference', __name__, template_folder='templates')
   

@bp.route('/cabinet/source_difference', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference():
    sour_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)     
    if request.method == 'POST':
        add = sour_diff_cntrl.add_source_difference_req(request)
        if add:
            flash('Додоано товар', category='success')
            return redirect('/cabinet/source_difference')
        else:
            flash('Товар не додано', category='success')
            return redirect('/cabinet/source_difference')
    else:
        product = sour_diff_cntrl.load_source_difference()
        print(f"Перевірка {product}")
        return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
     

@bp.route('/cabinet/source_difference/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_product(id):
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)   
    period = "month"  
    product = source_diff_cntrl.load_source_difference_id_period(id, period)
    if product:
        return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
    else:
        flash('Товар не знайдено', category='success')
        product = source_diff_cntrl.load_source_difference()
        print(f"Перевірка {product}")
        return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
      
   
@bp.route('/cabinet/source_difference/update_day', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_update_day():
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
    add_quantity = source_diff_cntrl.add_quantity_crm_today()   
    return redirect('/cabinet/source_difference')


@bp.route('/cabinet/source_difference/update/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_update(id):
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)   
    if request.method == 'POST': 
        print("Поехали")
        bool = source_diff_cntrl.update_source_diff_line(request, id) # данні є тільки в реквесті та айди це строки та
        print(f"Перевірка {bool}")
        return redirect('/cabinet/source_difference/{}'.format(request.form['source_id'])) 
    else:
        period = "month"  
        line = source_diff_cntrl.load_source_diff_line(id)
        if line:
            return render_template("cabinet_client/analitic/update_source_difference.html", line=line, user=current_user)
        else:
            flash('Товар не знайдено', category='success')
            product = source_diff_cntrl.load_source_difference()
            print(f"Перевірка {product}")
            return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
    
      