from flask import Flask, render_template
from auth import auth_blueprint
from blog import blog_blueprint
from comments import comments_blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(blog_blueprint, url_prefix='/blog')
app.register_blueprint(comments_blueprint, url_prefix='/comments')

@app.route('/')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
