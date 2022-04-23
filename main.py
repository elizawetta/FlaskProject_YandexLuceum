from flask import Flask, render_template
from data import db_session
from flask_login import LoginManager
import requests
from data.__all_models import *

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/reg')
def reg():
    return render_template("register.html")


@app.route('/user')
def user():
    return render_template("user.html")


if __name__ == '__main__':
    db_session.global_init("db/passwords.db")
    # db_session.
    app.run(port=8000, host='localhost')
