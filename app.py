from flask import Flask, render_template, request, redirect, url_for,\
    session, flash
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
        if 'name' in session:
            return f(*args, **kwargs)
        else:
            flash(' Sorry! You Need to Login to view this page')
            return redirect(url_for('login'))
    return wrap


def logout_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'name' in session:
            flash(
                ' Sorry! You are logged in Already. Logout to Do your Action')
            return redirect(url_for('home'))
        else:
            return f(*args, **kwargs)
    return wrap


def auth_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash(
                ' Sorry! You dont have any permission to perform such action')
            return redirect(url_for('home'))
    return wrap

# Controllers.


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
            flash(
                'ERROR! Please enter something or check yours\
                username or user already exists'
            )
            return redirect(url_for('register'))
        else:
            return redirect(url_for('home'))
    return render_template('forms/register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
    messages = models.message_show()
    return render_template('pages/placeholder.home.html', messages=messages)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/users')
@login_requied
def users():
    users = models.users()
    return render_template('pages/placeholder.users.html', users=users)


@app.route('/logout')
@login_requied
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
@logout_requied
def login():
    error = None
    session.clear()
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.name.data
        password = form.password.data
        value = flask_login_auth.authenticate(username, password)
        if (value == 1):
            role = flask_login_auth.role_authenticate(username, password)
            blocked = flask_login_auth.blocked(username, password)
            if not blocked:
                session['name'] = username
                session['role'] = role
                session['editid'] = None
                messages = models.message_show()
                return render_template('pages/placeholder.home.html',
                                       session=session, messages=messages)
            else:
                error = 'Your Account is blocked !\
                Please contact Admin'
                return render_template(
                    'forms/login.html', form=form, error=error)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('forms/login.html', form=form, error=error)
    return render_template('forms/login.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
@login_requied
def search():
    search = request.form['search']
    match = flask_login_auth.searchbox(search)
    print match
    return render_template('pages/placeholder.search.html', search=search,
                           match=match)


@app.route('/index')
@login_requied
def index():
    project = flask_login_auth.show_project(session['usersid'])
    session['project'] = project
    return render_template('pages/placeholder.home.html', session=session)


@app.route('/message', methods=['GET', 'POST'])
@login_requied
def message():
    if request.method == 'POST':
        models.post_messages(
            session['name'], request.form['message'])
        return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
@login_requied
def delete():
    if request.method == 'POST':
        models.message_delete(
            request.form['submit'])
        return redirect(url_for('home'))


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
        session['editid'] = request.form['submit']
        return redirect(url_for('update'))


@app.route('/update', methods=['GET', 'POST'])
@login_requied
def update():
    if session['editid']:
        userid = session['editid']
    else:
        userid = session['name']
    form = UpdateForm(request.form)
    get_info = models.get_info(userid)
    if request.method == 'POST':
        user = models.update(
            form.role.data, userid, form.password.data,
            form.email.data, form.name.data
        )
        if user != 1:
            flash(
                "ERROR! Already on this role, or you hadn't updated anything"
            )
            return redirect(url_for('update'))
        else:
            flash(
                'Successfully Role changed for  %s to %s' % (
                    userid, form.role.data)
            )
            session['editid'] = None
            return redirect(url_for('users'))
    return render_template(
        'forms/update.html', form=form, userid=userid, get_info=get_info
    )


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


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
    app.run(debug=False)
