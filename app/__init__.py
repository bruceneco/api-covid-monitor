from flask import Flask
from .commands import create_tables
from .extensions import db, migrate
from .routes.auth import auth
from .routes.health import health
from .routes.symptoms import symptoms


def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth)
    app.register_blueprint(symptoms)
    app.register_blueprint(health)
    print(app.url_map)
    app.cli.add_command(create_tables)

    return app
