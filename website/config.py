# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess-my-secret-key-1'
SECURITY_PASSWORD_SALT = 'you-will-never-guess-my-salt-1'

DEBUG = False
BCRYPT_LOG_ROUNDS = 13
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# email server
#MAIL_SERVER = 'your.mailserver.com'
#MAIL_PORT = 25
#MAIL_SERVER = 'smtp.googlemail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
#MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = 'tdbackes@gmail.com'
MAIL_PASSWORD = ''

# mail accounts
MAIL_DEFAULT_SENDER = 'tdbackes@gmail.com'

# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# administrator list
ADMINS = ['you@example.com']

# pagination
POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50

# Reload templates in production
TEMPLATES_AUTO_RELOAD = True
