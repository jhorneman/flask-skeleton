# This module encapsulates everything related to creating the Flask app, including selecting and
# loading configurations.
#
# The application's behavior depends on:
#   the RUN MODE - the role it's in,
#   the RUN ENVIRONMENT - where it's running (how it connects to external services), and
#   KILL SWITCHES - used to turn off certain features, overriding the run mode and the run environment
#
# The following run modes are supported:
#   dev        - for development.
#   test       - for automated testing.
#   production - for live operations.
#
# The run environment is only valid in production mode, and is set using the APP_RUN_ENV
# environment variable.
#
# The following run environments are supported:
#   local   - a developers' local machine.
#   heroku  - on Heroku or locally using Foreman.
#   vagrant - in a VM managed using Vagrant.

import os
import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from jinja_filters import set_up_jinja_filters
from .app_logging import set_up_logging


app = None  # Set to None so code will fail screaming if create_app hasn't been called
db = SQLAlchemy()


def create_app(_run_mode=None):
    # Create Flask app
    global app
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask("application", template_folder=template_dir)

    # Load kill switches
    # app.config["APP_KILL_CACHE"] = os.environ.get("APP_KILL_CACHE", False)

    # Load default configuration
    app.config.from_object("application.default_config")

    # Dev run mode
    if _run_mode == "dev":
        app.config["DEBUG"] = True

        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"    # Replace with local DB

        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False  # Otherwise this gets annoying real fast
        DebugToolbarExtension(app)

    # Test run mode
    elif _run_mode == "test":
        app.config["DEBUG"] = True
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False  # Or CSRF checks will fail
#        app.config["APP_KILL_CACHE"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # Production run mode
    elif _run_mode == "production":
        # Get additional configuration based on run environment
        run_environment = os.environ.get("APP_RUN_ENV", "local")
        if run_environment == "heroku":
            # Get configuration data from Heroku environment variables
            app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

        elif run_environment == "vagrant":
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"    # Replace with local DB

        set_up_logging(app)

    # Unrecognized run mode
    else:
        logging.error("Did not recognize run mode '%s'" % _run_mode)
        return None, None

    # Initialize the database
    global db
    import application.models
    db.init_app(app)

    # Initialize other Flask extensions

    # Import the views, to apply the decorators which use the global app object.
    import application.views

    # Register blueprints
    # from application.widget import widget_blueprint
    # app.register_blueprint(widget_blueprint)

    # Set up Jinja 2 filters
    set_up_jinja_filters(app)

    return app, db
