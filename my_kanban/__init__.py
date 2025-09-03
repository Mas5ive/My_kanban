import os

from flask import Flask, render_template
from flask_alembic import Alembic
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

sqla = SQLAlchemy()
jwt = JWTManager()
alembic = Alembic()


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    config_name = os.environ.get('FLASK_CONFIG', 'demo')
    app.config.from_mapping(
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_COOKIE_SECURE=False,
        JWT_COOKIE_CSRF_PROTECT=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config_name == 'development':
        app.config.from_mapping(
            SECRET_KEY='dev',
            JWT_SECRET_KEY='whoisyourdaddy',
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'dev_db.sqlite3'),
            SQLALCHEMY_ECHO=True,
        )
    elif config_name == 'demo':
        app.config.from_pyfile('config.py', silent=True)
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'demo_db.sqlite3'),
            SQLALCHEMY_ECHO=False
        )

    if test_config:
        app.config.from_mapping(test_config)

    sqla.init_app(app)
    jwt.init_app(app)
    alembic.init_app(app)

    from .routes import auth, board, card, comment, membership, profile
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(board.bp)
    app.register_blueprint(membership.bp)
    app.register_blueprint(card.bp)
    app.register_blueprint(comment.bp)

    from .scripts.commands import init_app, load_data
    init_app(app)

    if config_name == 'demo':
        with app.app_context():
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            db_path = db_uri.replace('sqlite:///', '')
            if not os.path.exists(db_path):
                alembic.upgrade()
                load_data.callback()

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
