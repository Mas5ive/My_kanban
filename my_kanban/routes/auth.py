from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_jwt_extended import (create_access_token, set_access_cookies,
                                unset_jwt_cookies)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from my_kanban import crud

bp = Blueprint('auth', __name__, url_prefix='/auth')


def redirect_to_profile(identity):
    response = redirect(url_for("profile.show"))
    access_token = create_access_token(identity=identity)
    set_access_cookies(response, access_token)
    return response


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                crud.create_user(username, password)
            except IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect_to_profile(username)

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = crud.get_user_by_name(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.psw_hash, password):
            error = 'Incorrect password.'

        if error is None:
            return redirect_to_profile(username)

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    return response
