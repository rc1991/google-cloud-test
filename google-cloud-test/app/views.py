import logging
from functools import wraps
from flask import render_template, url_for, redirect, g, request
from main import app
from model import Account
from google.appengine.api import users


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = users.get_current_user()
        if user:
            account = Account.query(Account.userid == user.user_id()).fetch(1)
            if account:
                g.user = account[0]
                logging.info('Existed account, key:'+str(account[0].key.id()))
            else:
                logging.info("New account, google user id:"+str(user.user_id()))
                new_account = Account(userid=user.user_id(), username=user.nickname(), email=user.email())
                new_account_key = new_account.put()
                logging.info('New account, key:'+ str(new_account.key.id()))
                g.user = new_account
        else:
            url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(url)
            return redirect(url)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    username = g.user.username
    url = users.create_logout_url('/')
    greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(username, url)
    return render_template('base.html', username=username, email=g.user.email, userid=g.user.userid, logout_url=url)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


