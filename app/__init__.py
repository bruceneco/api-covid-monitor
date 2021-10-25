from flask import Flask
from .commands import create_tables
from .extensions import db, migrate
from .routes.auth import auth


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth)
    print(app.url_map)
    app.cli.add_command(create_tables)

    return app
