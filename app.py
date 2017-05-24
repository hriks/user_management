from flask import Flask, render_template as render,\
    request, redirect, url_for,\
    session as s
from flask import flash as hriks
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
import models
from functools import wraps
import flask_login_auth
from forms import *
import logging


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config.from_object('config')
db = SQLAlchemy(app)


# Decorator's


def login_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in s:
            return f(*args, **kwargs)
        else:
            hriks(' Sorry! You Need to Login to view this page')
            return redirect(url_for('login'))
    return wrap


def logout_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in s:
            hriks(
                'Sorry! You are already logged in. Logout to perform your\
                 Action'
            )
            return redirect(url_for('home'))
        else:
            return f(*args, **kwargs)
    return wrap


def auth_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if s['role'] == 'admin':
            return f(*args, **kwargs)
        else:
            hriks(
                ' Sorry! You dont have any permission to perform such action')
            return redirect(url_for('home'))
    return wrap


# Controllers.


# user will be able to register new user when logged in
# as Admin or manager
@app.route('/register', methods=['GET', 'POST'])
@login_requied
@auth_requied
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = models.create_user(
            form.userid.data, form.name.data, form.role.data,
            form.email.data, form.password.data
        )
        if user == 1:
            hriks(
                'ERROR! Please enter something or check yours\
                username and password or user already exists'
            )
            return redirect(url_for('register'))
        else:
            return redirect(url_for('home'))
    return render('forms/register.html', form=form)


# user will be able to register new user as normal
# user without login with only user role
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        user = models.create_user(
            form.userid.data,
            form.name.data,
            form.role.data,
            form.email.data,
            form.password.data
        )
        if user == 1:
            hriks(
                'ERROR! Please enter something or check yours\
                username and password or user already exists'
            )
            return redirect(url_for('register'))
        else:
            return redirect(url_for('home'))
    return render('forms/register.html', form=form)


# Open as you run the server
@app.route('/', methods=['GET', 'POST'])
def home():
    messages = models.message_show()
    return render('pages/placeholder.home.html', messages=messages, session=s) # noqa


@app.route('/about')
def about():
    return render('pages/placeholder.about.html')


# Shows all user
@app.route('/users')
@login_requied
def users():
    users = models.users()
    return render('pages/placeholder.users.html', users=users)


# Logout user
@app.route('/logout')
@login_requied
def logout():
    s.clear()
    return redirect(url_for('home'))


# This implifies for login and authentication
# for user, role, blocked, and also count
# no if time user is logged in
@app.route('/login', methods=['GET', 'POST'])
@logout_requied
def login():
    error = None
    s.clear()
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.name.data
        print username
        password = form.password.data
        print password
        value = flask_login_auth.authenticate(username, password)
        print value
        if (value == 1):
            role = flask_login_auth.role_authenticate(username, password)
            blocked = flask_login_auth.blocked(username, password)
            # Checks user is blocked
            # and return value in true or
            # False
            if not blocked:
                s['name'] = username
                s['role'] = role
                s['editid'] = None
                # count will show no of time user logged in
                count = models.count_show(username)
                messages = models.message_show()
                if count[0][0]:
                    s['count'] = count[0][0] + 1
                    new_count = s['count']
                new_count = models.count_add(username, new_count)
                models.count_show(username)
                return render('pages/placeholder.home.html', session=s, messages=messages) # noqa
            else:
                error = 'Your Account is blocked !\
                Please contact Admin'
                return render(
                    'forms/login.html', form=form, error=error)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render('forms/login.html', form=form, error=error)
    return render('forms/login.html', form=form)


# client will be able to search by username
@app.route('/search', methods=['GET', 'POST'])
@login_requied
def search():
    search = request.form['search']
    match = flask_login_auth.searchbox(search)
    print match
    return render(
        'pages/placeholder.search.html', search=search,
        match=match
    )


@app.route('/index')
@login_requied
def index():
    if 'userid' in s:
        project = flask_login_auth.show_project(s['usersid'])
        s['project'] = project
        return render('pages/placeholder.home.html', session=s)
    else:
        return redirect(url_for('home'))


# Post messages on Dashboard
# This can be done by any user
@app.route('/message', methods=['GET', 'POST'])
@login_requied
def message():
    if request.method == 'POST':
        models.post_messages(
            s['name'], request.form['message'])
        return redirect(url_for('home'))


# Admin will able to delete messages posted
# on Dashboard
@app.route('/delete', methods=['GET', 'POST'])
@login_requied
def delete():
    if request.method == 'POST':
        models.message_delete(
            request.form['submit'])
        return redirect(url_for('home'))


# Admin able to block the user ny using this method
@app.route('/block', methods=['GET', 'POST'])
@login_requied
def block():
    if request.method == 'POST':
        models.block(
            request.form['submit'], request.form['userid'])
        return redirect(url_for('users'))


@app.route('/edit', methods=['GET', 'POST'])
@login_requied
def edit():
    if request.method == 'POST':
        s['editid'] = request.form['submit']
        return redirect(url_for('update'))


@app.route('/update', methods=['GET', 'POST'])
@login_requied
def update():
    if 'editid' in s:
        userid = s['editid']
    else:
        userid = s['name']
    form = UpdateForm(request.form)
    get_info = models.get_info(userid)
    if request.method == 'POST':
        user = models.update(
            form.role.data, userid, form.password.data,
            form.email.data, form.name.data
        )
        if user != 1:
            hriks(
                "ERROR! Already on this role, or you hadn't updated anything"
            )
            return redirect(url_for('update'))
        else:
            hriks(
                'Successfully role changed for  %s to %s' % (
                    userid, form.role.data)
            )
            s['editid'] = None
            return redirect(url_for('users'))
    return render(
        'forms/update.html', form=form,
        userid=userid, get_info=get_info
    )


# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    # db_s.rollback()
    return render('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('% (asctime)s % (levelname)s: % (message)s\
                  [in % (pathname)s: % (lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# Default port:
if __name__ == '__main__':
    app.run(debug=True)
