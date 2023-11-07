from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

auth_blueprint = Blueprint('auth', __name__)

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

SECRET_KEY = 'Allah'

def init_auth(app):
    @auth_blueprint.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            with app.app_context(): 
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('User with this email already exists', 'danger')
                    return redirect(url_for('auth.register'))

                hashed_password = generate_password_hash(password, method='sha256')

                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('registration.html')

    @auth_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            with app.app_context(): 
                user = User.query.filter_by(email=email).first()

                if user and check_password_hash(user.password, password):
                    token = jwt.encode({'email': user.email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256')

                    flash('Login successful! Your JWT token: ' + token.decode('utf-8'), 'success')
                else:
                    flash('Login failed. Check your email and password.', 'danger')

        return render_template('login.html')
