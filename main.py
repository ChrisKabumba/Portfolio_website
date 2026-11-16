from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, logout_user
from models import db, User, Project
from forms import *
import os

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

db.init_app(app)

with app.app_context():
    db.create_all()

Bootstrap5(app)
ckeditor = CKEditor(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)



@app.route('/')
def index():

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)