from flask import Blueprint, redirect, render_template, request, flash, redirect, url_for, jsonify, session
from server_flask.models import Comment, Posts, Reply, Reply2, Users
from flask_login import login_required, current_user
from server_flask.db import db
import sys

# from app.utils.auth import login_required

bp = Blueprint('Blog', __name__, template_folder='templates')



@bp.route('/blog', methods=['POST', 'GET'])
@login_required
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

@bp.route('/blog/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Posts.query.get_or_404(id)
    try:
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return redirect('/blog')
    except:
        return 'There was an issue deleting that task'

@bp.route('/blog/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task_update = Posts.query.get_or_404(id)

    if request.method == 'POST':
        task_update.text = request.form['content']
        try:
            db.session.commit()
            print(">>> Update in datebase")
            return redirect('/blog')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('blog_update.html', task=task_update)

@bp.route('/blog/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        task_name_post = request.form['name_post']
        task_content = request.form['content']
        author_id = current_user
        if not task_content:
            flash('Post cannot be empty', category='error')
        else:
            post = Posts(name_post=task_name_post, text=task_content, author_id=author_id.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('Blog.Blog'))

    return render_template('add_post.html', user=current_user)