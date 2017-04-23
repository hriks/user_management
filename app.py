from flask import Flask, render_template, request, redirect, url_for,\
    session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from models import User, Projects, Pledges
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
            flash(' Sorry! You are logged in Already. Logout to Do your Action')
            return redirect(url_for('home'))
        else:
            return f(*args, **kwargs)
    return wrap


def forget_step1(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'step1' in session:
            return f(*args, **kwargs)
        else:
            flash(' Sorry! You Need to Verify Email First')
            return redirect(url_for('login'))
    return wrap


def forget_step2(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'step2' in session:
            return f(*args, **kwargs)
        else:
            flash(' Sorry! You Need to Verify Email First')
            return redirect(url_for('login'))
    return wrap

# Controllers.


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


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
            get_data = flask_login_auth.get_data(username, password)
            session['name'] = username
            session['usersid'] = get_data[0][0]
            project = flask_login_auth.show_project(session['usersid'])
            session['project'] = project
            return render_template('pages/placeholder.home.html',
                                   session=session)
        else:
            error = 'Invalid username or password \
            Please try again!'
            return render_template('forms/login.html', form=form, error=error)
    return render_template('forms/login.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_requied
def create():
    form = CreateProject(request.form)
    if request.method == 'POST':
        project = Projects(session['usersid'],
                           form.name.data, form.short_desc.data,
                           form.long_desc.data, form.goal_amount.
                           data, form.time_end.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pages/placeholder.create.html', form=form)


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


@app.route('/showPledge', methods=['GET', 'POST'])
@login_requied
def showPledge():
    if request.method == 'POST':
        projectId = request.form['submit']
        session['projectId'] = projectId
        return redirect(url_for('newPledge'))


@app.route('/newPledge', methods=['GET', 'POST'])
@login_requied
def newPledge():
    form = NewPledge(request.form)
    if request.method == 'POST':
        pledge = Pledges(session['projectId'],
                         session['usersid'], form.amount.data)
        db.session.add(pledge)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('pages/placeholder.pledge.html', form=form,
                           session=session)


@app.route('/register', methods=['GET', 'POST'])
@logout_requied
def register():
    session.clear()
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = User(form.name.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)


@app.route('/forgot', methods=['GET', 'POST'])
@logout_requied
def forgot():
    session.clear()
    form = ForgotForm(request.form)
    if request.method == 'POST':
        email = form.email.data
        step1 = flask_login_auth.verify_email(email)
        if step1 == 1:
            session['step1'] = email
            return redirect(url_for('verification_step2'))
    return render_template('forms/forgot.html', form=form)


@app.route('/verification_step2', methods=['GET', 'POST'])
@forget_step1
def verification_step2():
    form = ForgotForm2(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = flask_login_auth.verify_user(username)
        session['step2'] = username
        session['step2'] = password
        print password
        return redirect(url_for('get_data'))
    return render_template('forms/forgot_2.html', form=form, session=session)


@app.route('/get_data', methods=['GET', 'POST'])
@forget_step1
def get_data():
    return render_template('pages/placeholder.forget.html', session=session)

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
    app.run(debug=True)
