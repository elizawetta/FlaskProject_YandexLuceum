from flask import render_template, redirect, Flask, request
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.__all_models import *
import hashing as hsh

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/user")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
    # return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        if not db_sess.query(User).filter(User.login == request.form['login']).all():
            if request.form['password'].strip() == '' or request.form['login'].strip() == '':
                return render_template("register.html", status='Введите корректные данные')
            new_user = User()
            new_user.login = request.form['login']
            new_user.salt, new_user.hash_password = hsh.make_hash_password(request.form['password'])
            new_user.password = request.form['password']
            db_sess.add(new_user)
            db_sess.commit()
        else:
            return render_template("register.html", status='Пользователь с таким именем существует')
        return redirect('/login')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    passwords = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id).all()
    if request.method == "GET":
        return render_template("user.html", user=current_user.login, passwords=passwords)
    elif request.method == "POST":
        if request.form['password'].strip() == '' or request.form['login'].strip() == '':
            return render_template("user.html", user=current_user.login, passwords=passwords,
                                   message="Введите корректные данные")

        p = Passwords()
        p.user_id = current_user.id
        p.password = request.form['password']
        p.cite = request.form['login']
        db_sess.add(p)
        db_sess.commit()
        passwords = db_sess.query(Passwords).filter(Passwords.user_id == current_user.id).all()
        return render_template("user.html", user=current_user.login, passwords=passwords)


if __name__ == '__main__':
    db_session.global_init("db/passwords.db")
    db_sess = db_session.create_session()
    app.run(port=8000, host='localhost')
