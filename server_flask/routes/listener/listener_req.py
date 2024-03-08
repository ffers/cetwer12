from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for, jsonify, session

bp = Blueprint('Listener', __name__, template_folder='templates')

@bp.route('/orders', methods=['POST'])
def Blog():
    if request.method == 'POST':
        task_content = request.form['content']
        task_name_post = request.form['name_post']
        new_task = Posts(text=task_content, name_post=task_name_post)
        #        try:
        db.session.add(new_task)
        db.session.commit()
        print(">>> Add datebase")
        return redirect('/blog')
    else:
        tasks_posts = Posts.query.order_by(Posts.timestamp).all()
        tasks_users = Users.query.order_by(Users.timestamp).all()
        return render_template('blog.html', tasks_users=tasks_users, posts=tasks_posts,  user=current_user)


