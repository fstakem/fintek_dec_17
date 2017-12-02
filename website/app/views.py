
from flask import Flask
from flask import render_template, flash, redirect, session, url_for, request, g
from flask import abort

from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from flask_login import LoginManager

from flask_babel import gettext
from flask_babel import lazy_gettext

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose

from datetime import datetime
from functools import wraps

from app import app, db, lm, oid, babel
from app import models

from .forms import LoginForm, EditForm, PostForm, SearchForm, NewPaymentForm
from .models import User, Post, Payment
from .emails import follower_notification
from .emails import send_email
from .emails import send_email_confirmation
from .token import generate_confirmation_token, confirm_token
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from config import LANGUAGES

from .load_data import DataLoader

#from urlparse import urlparse, urljoin
from urllib.parse import urljoin, urlparse

from sqlalchemy import desc

from flask_wtf.csrf import CSRFProtect

import math
import sys

admin = Admin(app)
#csrf = CSRFProtect(app)

# This commented out code is the start of a roles based security for the admin views
# Change the decorator for login_required to allow for user roles
# def login_required(role="ANY"):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated():
#                return current_app.login_manager.unauthorized()
#             urole = current_app.login_manager.reload_user().get_user_role()
#             if ( (urole != role) and (role != "ANY")):
#                 return current_app.login_manager.unauthorized()      
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper
# def login_required(role="ANY"):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorated_view(*args, **kwargs):
#             if not current_user.is_authenticated():
#               return lm.unauthorized()
#             if ((current_user.role != role) and (role != "ANY")):
#                 return lm.unauthorized()
#             return fn(*args, **kwargs)
#         return decorated_view
#     return wrapper


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))
    posts = None
    return render_template('index.html',
                           title='Home',
                           form=form,
                           posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():
    print('starting view for login', file=sys.stderr)
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if not registered_user:
        flash('Username is invalid', 'error')
        print('Username is invalid', file=sys.stderr)
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        print('Password is invalid', file=sys.stderr)
        return redirect(url_for('login'))
    login_user(registered_user, remember = remember_me)

    next = request.args.get('next')
    # is_safe_url should check if the url is safe for redirects.
    # See http://flask.pocoo.org/snippets/62/ for an example.
    #if not is_safe_url(next):
    #    print('next URL is not safe', file=sys.stderr)
    #    return abort(400)

    flash('Logged in successfully')

    return redirect(next or url_for('index'))


@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    print('User successfully registered', file=sys.stderr)
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.route('/register_user' , methods=['GET','POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username', None)
    password = request.form.get('password', None)
    email = request.form.get('email', None)

    if not username:
        flash('Invalid user name')

    if username and password and email:
        # Valid details. Try to create account.
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        print('User successfully registered', file=sys.stderr)
        flash('User successfully registered')
        return redirect(url_for('login'))

    if not username:
        flash('Invalid user name')
    if not password:
        flash('Invalid password')
    if not email:
        flash('Invalid email')

    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/user_page/<username>')
@app.route('/user_page/<username>/<int:page>')
@login_required
def user_page(username, page=1):
    user = User.query.filter_by(username=username).first()
    if not user:
        print('user is None', file=sys.stderr)
        flash(gettext('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    print('user is not None', file=sys.stderr)
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user_page.html',
                           user=user,
                           posts=posts)


# Legacy social code
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        g.user.email = form.email.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        form.email.data = g.user.email
    return render_template('edit.html', form=form)


# Legacy social code
@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if not u:
        flash(gettext('Cannot follow %(nickname)s.', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(nickname)s!', nickname=nickname))
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


# Legacy social code
@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if not user:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if not u:
        flash(gettext('Cannot unfollow %(nickname)s.', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stopped following %(nickname)s.',
                  nickname=nickname))
    return redirect(url_for('user', nickname=nickname))


@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)


@app.route('/create_payment', methods=['GET', 'POST'])
@login_required
def create_payment():
    form = NewPaymentForm(g.user.nickname)
    if form.validate_on_submit():
        payment = Payment(payment_name=form.payment_name.data, owner_id=g.user.id)
        payment.payment_description = form.description.data
        db.session.add(payment)
        db.session.commit()
        flash(gettext('Created payment %(payment_name)s.', payment_name=form.payment_name.data))
        return redirect(url_for('index'))
    elif request.method != "POST":
        form.payment_name.data = 'NewPayment'
    return render_template('create_payment.html', form=form)





@app.route('/load_data', methods = ['POST', 'GET'])
@app.route('/load_data/<action>', methods = ['POST', 'GET'])
@login_required
def load_data(action='none'):

    if request.method == 'POST':
        # User selected the load data button
        print('User pressed load data button', file=sys.stderr)
        print('action : %s' % action, file=sys.stderr)

        if(action=='load_questions'):
            print('Loading questions', file=sys.stderr)

            dl = DataLoader()
            pl = dl.load_data()

            for p in pl:
                db.session.add(q)
                db.session.commit()

        elif(action=='purge_data'):
            print('Purging data', file=sys.stderr)
            payments = Payment.query
            for p in payments:
                db.session.delete(p)
                db.session.commit()

    number = 0
    return render_template("load_data.html", number=number)


@app.route('/send_confirmation_email', methods = ['POST', 'GET'])
@app.route('/send_confirmation_email/<username>', methods = ['POST', 'GET'])
@login_required
def send_confirmation_email():
    user = g.user
    token = generate_confirmation_token(user.email)

    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email_confirmation(to=user.email, subject=subject, template=html)

    flash('A confirmation email has been sent via email.', 'success')
    return redirect(url_for("index"))


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('user_page',username=user.username))


class TestView(ModelView):
    # Disable model creation
    can_create = True
    # Override displayed fields
    column_list = ('username', 'password')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(TestView, self).__init__(User, session, **kwargs)


class UserView(ModelView):
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        return self.render('index.html')


# Admin views
# Need to add login requirement to these views and add an admin user role
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
admin.add_view(ModelView(models.Payment, db.session))


