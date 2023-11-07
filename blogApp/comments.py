from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import jwt_required, current_identity
from datetime import datetime


comments_blueprint = Blueprint('comments', __name__)

# Define database models using SQLAlchemy
db = SQLAlchemy()

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@comments_blueprint.route('/add_comment/<int:post_id>', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    if request.method == 'POST':
        text = request.form['text']

        new_comment = Comment(text=text, author_id=current_identity.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully', 'success')
        return redirect(url_for('comments.add_comment', post_id=post_id))

    return render_template('add_comment.html', post_id=post_id)

@comments_blueprint.route('/view_comments/<int:post_id>')
def view_comments(post_id):
    post_comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('view_comments.html', post_id=post_id, comments=post_comments)
