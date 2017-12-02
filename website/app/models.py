from hashlib import md5
import re
from app import db
from app import app
from datetime import datetime
from datetime import timedelta
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
import sqlalchemy
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from random import randrange

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask_whooshalchemy

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(64), index=True, unique=True)
    password = db.Column('password', db.String(250), index=True, unique=False)
    user_role = db.Column('user_role', db.String(64), index=True, unique=False)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirmed = db.Column(db.Boolean, index=False, unique=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    registered_on = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    payments = db.relationship('Payment', backref='owner', lazy='dynamic')

    def __init__(self, username = 'NA', password = 'NA', \
                 user_role = 'user', \
                 nickname = None, email = None, posts = None, \
                 about_me = None,  last_seen = None, registered_on = None, followed = None, \
                 email_confirmed=False):
        self.username = username
        #self.password = password
        self.set_password(password)
        self.registered_on = datetime.utcnow()
        self.last_seen = last_seen
        self.about_me = about_me
        self.email = email
        self.nickname = nickname
        self.email_confirmed = email_confirmed

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        #return unicode(self.id)
        return str(self.id)

    def get_user_role(self):
            return self.user_role

    def __repr__(self):
        return '<User %r>' % (self.username)

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
            (md5(self.email.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % (self.username)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    payment_name = db.Column(db.String(64), index=True, unique=False)
    payment_description = db.Column(db.String(250), index=False, unique=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_created = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    def __repr__(self):
        return '<Payment %r>' % (self.payment_name)

    def __init__(self, payment_name = 'New payment', owner_id = None, owner_username = None):
        self.payment_name = payment_name
        self.owner_id = owner_id
        self.date_created = datetime.utcnow()
        self.last_modified = datetime.utcnow()


def __init__(self, client_socket=None, statusMessage=""):
    self.client_socket = client_socket
    self.statusMessage = statusMessage


if enable_search:
    whooshalchemy.whoosh_index(app, Post)
