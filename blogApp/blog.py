from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import jwt_required, current_identity
from datetime import datetime

blog_blueprint = Blueprint('blog', __name__)

db = SQLAlchemy()

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@blog_blueprint.route('/create_post', methods=['GET', 'POST'])
@jwt_required()
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = BlogPost(title=title, content=content, author_id=current_identity.id)
        db.session.add(new_post)
        db.session.commit()

        flash('Blog post created successfully', 'success')
        return redirect(url_for('blog.create_post'))

    return render_template('create_post.html')

@blog_blueprint.route('/posts')
def view_posts():
    posts = BlogPost.query.all()
    return render_template('view_posts.html', posts=posts)
