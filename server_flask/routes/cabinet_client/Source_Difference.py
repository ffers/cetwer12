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
            flash('Додано товар', category='success')
            return redirect('/cabinet/source_difference')
        else:
            flash('Товар не додано', category='success')
            return redirect('/cabinet/source_difference')
    else:
        product = sour_diff_cntrl.load_source_difference()
        print(f"Перевірка {product}")
        return render_template("cabinet_client/analitic/source_difference.html", product=[], user=current_user)
       

@bp.route('/cabinet/source_difference/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_product(id):
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)   

    product = source_diff_cntrl.load_source_difference_id_period(id, "days", 30)
    if product:
        return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
    else:
        flash('Товар не знайдено', category='error')
        product = source_diff_cntrl.load_source_difference()
        print(f"Перевірка {product}")
        return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)

     
@bp.route('/cabinet/source_difference/update_day', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_update_day():
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
    # add_line_diff = source_diff_cntrl.add_quantity_crm_today()
    # add_quantity = source_diff_cntrl.sour_diff_all_source_sold("two_days") 
    source_diff_sum = source_diff_cntrl.update_source_difference_period("month")
    return redirect('/cabinet/source/all')
  

@bp.route('/cabinet/source_difference/update/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_update(id):
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)   
    if request.method == 'POST': 
        print("Поехали")
        bool = source_diff_cntrl.update_source_diff_line(request, id) # данні є тільки в реквесті та айди строки 
        print(f"Перевірка {bool}")
        return redirect('/cabinet/source_difference/{}'.format(request.form['source_id'])) 
    else:
        period = "month"  
        line = source_diff_cntrl.load_source_diff_line(id)
        if line:
            return render_template("cabinet_client/analitic/update_source_difference.html", line=line, user=current_user)
        else:
            flash('Товар не знайдено', category='error')
            product = source_diff_cntrl.load_source_difference()
            print(f"Перевірка {product}")
            return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
        
@bp.route('/cabinet/source_difference/delete/<int:id>', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_delete(id):
    print("Видалення")
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
    resp = source_diff_cntrl.delete(id)
    return redirect('/cabinet/source_difference/{}'.format(resp[1]))
        
 

@bp.route('/cabinet/source_difference/update_bulk', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_diff_update_bulk():
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
    add = source_diff_cntrl.update_sour_diff_table(request.get_json())
    if add:
        flash('Оновлено', category='success')
        return "OK", 200
    else:
        flash('Невийшло', category='error')
        return 400
    

@bp.route('/cabinet/source_difference/load_event_day', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_diff_load_event_day():
    if request.method == "POST":
        source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
        product = source_diff_cntrl.load_source_diff_event_date(request)
        if product:            
            return render_template("cabinet_client/analitic/source_difference.html", product=product, user=current_user)
        else:
            flash('Невийшло', category='error')
            return 400
        

@bp.route('/cabinet/source_difference/update_sold', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_diff_update_sold():
    if request.method == "GET":
        source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
        product = source_diff_cntrl.sour_diff_all_source_sold("month")
        if product:            
            return redirect('/cabinet/source/all')
        else:
            flash('Невийшло', category='error')
            return 400
         
 
@bp.route('/cabinet/source_difference/delete_event_day', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_diff_delete_event_day():
    if request.method == "POST":
        source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
        product = source_diff_cntrl.delete_event_date(request)
        if product:            
            return redirect('/cabinet/source/all')
        else:
            flash('Невийшло', category='error')
            return 400
         
@bp.route('/cabinet/source_difference/add_day', methods=['POST','GET'])
@login_required
@admin_permission.require(http_exception=403)   
def source_difference_add_day():
    source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
    add_line_diff = source_diff_cntrl.add_quantity_crm_today()
    return redirect('/cabinet/source/all')

# @bp.route('/cabinet/source_difference/test_button', methods=['POST','GET'])
# @login_required
# @admin_permission.require(http_exception=403)   
# def test_button():
#     source_diff_cntrl = get_instance('sour_diff_an_cntrl', SourDiffAnCntrl)
#     add_line_diff = source_diff_cntrl.add_quantity_crm_today()
#     return redirect('/cabinet/source/all')