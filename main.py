from flask import Flask, render_template, redirect
from data import db_session
from flask_login import LoginManager, login_user
import requests
from flask import Flask, url_for, request
from data.__all_models import *
import hashing as hsh

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
    # form = LoginForm()
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     user = db_sess.query(User).filter(User.login == form.login.data).first()
    #     if user and user.check_password(form.password.data):
    #         login_user(user, remember=form.remember_me.data)
    #         return redirect("/")
    #     return render_template('login.html',
    #                            message="Неправильный логин или пароль",
    #                            form=form)
    # return render_template('login.html', title='Авторизация', form=form)
    return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        new_user = User()
        new_user.login = request.form['login']
        new_user.salt, new_user.hash_password = hsh.make_hash_password(request.form['password'])
        new_user.password = request.form['password']
        db_sess.add(new_user)
        db_sess.commit()
        return redirect('/login')


@app.route('/user')
def user():
    return render_template("user.html")


if __name__ == '__main__':
    db_session.global_init("db/passwords.db")
    db_sess = db_session.create_session()
    app.run(port=8000, host='localhost')
