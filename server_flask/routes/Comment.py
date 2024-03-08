from flask import Blueprint, redirect, render_template, request, jsonify, session, flash
from server_flask.models import Comment, Posts, Reply, Reply2, Users
from server_flask.db import db
import sys

bp = Blueprint('comment', __name__, template_folder='templates')

@bp.route("/comments", methods=['POST', 'GET'])
def comments():
    if request.method == 'POST':
        text = request.form['comment']
        if not text:
            flash('Post cannot be empty', category='error')
        else:
            new_task = Comment(text=text)
            db.session.add(new_task)
            db.session.commit()
            print(">>> Add datebase")
            return redirect('/comments')
    else:
        comments = Comment.query.order_by(Comment.timestamp).all()
        reply = Reply.query.order_by(Reply.timestamp).all()
        return render_template('comments.html', comments=comments, reply=reply)

@bp.route('/add_reply/<int:parent_id>', methods=['GET', 'POST'])
def add_reply(parent_id):
    # Обработка формы для ответа на комментарий с ID comment_id
    if request.method == 'POST':
        reply_text = request.form.get('reply_text')
        # Добавьте код для сохранения ответа и комментария в базу данных
        new_task = Reply(text=reply_text, comment_id=parent_id)

#        try:
        db.session.add(new_task)
        db.session.commit()
        print(">>> Add datebase")
        return redirect('/comments')
    return render_template('add_reply.html', parent_id=parent_id)

@bp.route('/add_reply2/<int:parent_id>', methods=['GET', 'POST'])
def add_reply2(parent_id):
    # Обработка формы для ответа на комментарий с ID comment_id
    if request.method == 'POST':
        reply_text = request.form.get('reply_text')
        # Добавьте код для сохранения ответа и комментария в базу данных
        new_task = Reply2(text=reply_text, comment_id=parent_id)

#        try:
        with app.app_context():
            db.session.add(new_task)
            db.session.commit()
            print(">>> Add datebase 2")
            return redirect('/comments')
    return render_template('add_reply2.html', parent_id=parent_id)

@bp.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Comment.query.get_or_404(id)
    try:
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return redirect('/')
    except:
        return 'There was an issue deleting that task'