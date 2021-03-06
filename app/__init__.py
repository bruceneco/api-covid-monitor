from flask import Flask
from flask_cors import CORS

from .commands import create_tables, drop_tables
from .extensions import db, migrate
from .routes.auth import auth
from .routes.health import health
from .routes.symptoms import symptoms
from .routes.user import user


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    CORS(app)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth)
    app.register_blueprint(symptoms)
    app.register_blueprint(health)
    app.register_blueprint(user)

    app.cli.add_command(create_tables)
    app.cli.add_command(drop_tables)

    return app
