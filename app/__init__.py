from flask import Flask
from flask_migrate import Migrate

from .commands import create_tables
from .extensions import db
from .routes.auth import auth


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    Migrate(app, db)
    db.init_app(app)

    app.register_blueprint(auth)
    print(app.url_map)
    app.cli.add_command(create_tables)

    return app