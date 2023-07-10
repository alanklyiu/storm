# Third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Local imports
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Flask 1.0 added the builtin config value, ENV, to reflect the FLASK_ENV
# environment variable. Setting FLASK_ENV to development also enables debug
# mode, FLASK_DEBUG=1.
#
# We preload the config defined by ENV, then override it from a file in the
# instance folder, if it exists (update '.gitignore' to include the instance
# folder).
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[app.config['ENV']])
    app.config.from_pyfile('config.py', silent=True)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    from . import models

    from .errors import errors_bp
    app.register_blueprint(errors_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .home import home_bp
    app.register_blueprint(home_bp)

    return app