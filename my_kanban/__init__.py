import os

from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

sqla = SQLAlchemy()
jwt = JWTManager()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_COOKIE_SECURE=False,
        JWT_COOKIE_CSRF_PROTECT=False,
        JWT_SECRET_KEY='whoisyourdaddy',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3'),
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    sqla.init_app(app)
    jwt.init_app(app)

    from .data.db import init_app
    init_app(app)

    from . import auth, board, card, comment, membership, profile
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(board.bp)
    app.register_blueprint(membership.bp)
    app.register_blueprint(card.bp)
    app.register_blueprint(comment.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
