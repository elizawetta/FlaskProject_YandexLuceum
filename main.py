from flask import Flask, render_template, url_for

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/reg')
def reg():
    return render_template("register.html")

@app.route('/user')
def user():
    return render_template("user.html")


if __name__ == '__main__':
    app.run(port=8000, host='localhost')
