# This module encapsulates everything related to selecting and loading configurations,
# creating the Flask app, and running it.
#
# We need the following run modes:
#   dev - local, personal development server.
#   team - still local server, for development by team (specifically non-coder team members).
#   production - deployed on Heroku.
#
# Don't use environment variables for local configurations.
# Environment variables are annoying to set locally (global machine changes for a single project).
# Also we need to be able to run multiple servers on one machine (for dev/team).
#
# For production configuration, use whichever environment variables Heroku provides.
# But isolate this so it can be easily changed if we need to deploy somewhere else.
#
# Make production the default configuration so we never run in debug mode on the server by
# accident. 
#
# Isolate secrets and make it so they're only deployed if necessary
# (Can't really think of anything - there are secrets but they're needed in production. But
#  keep it mind.)
#
# Bundle default and per-configuration settings in clear places.
#
# Running the app also depends on the configuration. So we can't just create the app here,
# we also need to run it.
#
# If this code grows we could move it into its own module instead of __init__.

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# Set to None so code will fail screaming if run_app hasn't been called
app = None
app_run_args = {}

db = SQLAlchemy()

def create_app(_run_mode = "production"):
    # Create Flask app
    global app
    app = Flask("application")

    # Load default configuration
    app.config.from_object('application.default_config')

    # app.debug and app.config["DEBUG"] do the same thing. app.debug defaults to False.
    # To be extra sure default_config doesn't change this behavior, we set it to False again,
    # because we want to make sure we don't run debug in production by accident.
    app.config["DEBUG"] = False

    # (In the latest version of Flask we could set port and host to None so the Flask defaults will
    # be used we don't change these variables.)
    global app_run_args
    app_run_args = {'port': 5000, 'host': '127.0.0.1'}

    # Dev run mode
    if _run_mode == "dev":
        app.config["DEBUG"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        toolbar = DebugToolbarExtension(app)

    # Team run mode
    elif _run_mode == "team":
        app.config["DEBUG"] = True
        app_run_args['port'] = 5001

    # Production run mode
    elif _run_mode == "production":
        # Get port number from Heroku environment variable
        app_run_args['port'] = int(os.environ['PORT'])

    # Unrecognized run mode
    else:
        #TODO: Report error
        return

    # Initialize the database
    global db
    db.init_app(app)

    # Initialize application
    # Import the views, to apply the decorators which use the global app object.
    import application.views

def run_app():
    # Run the application
    # See flask/app.py run() for the implementation of run().
    # See http://werkzeug.pocoo.org/docs/serving/ for the parameters of Werkzeug's run_simple().
    # If debug is not set, Flask does not change app.debug, which we've already set above.
    app.run(**app_run_args)
