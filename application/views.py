from flask import render_template
from application import app, db
from application.models import User

@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()

@app.route('/')
def index():
	users = User.query.all()
	return render_template('show_users.html', users=users)
