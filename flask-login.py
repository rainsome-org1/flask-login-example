import os
from flask import Flask
from flask import render_template
from flask import request, abort
from flask.ext.login import LoginManager, login_user, login_required, logout_user
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
from flask import abort, redirect, url_for

app = Flask(__name__)

# Needed to csrf token included in wtforms http://es.wikipedia.org/wiki/Cross_Site_Request_Forgery
app.config['SECRET_KEY'] = "peper"	

# Init login manager
login_manager = LoginManager()
login_manager.init_app(app)

# This is a fake database with mails and passwords.
users_database = [
	{
		"mail": "user1@example.com",
		"password" : "user1"
	},
	{
		"mail": "user2@example.com",
		"password" : "user2"
	},
	{
		"mail": "user3@example.com",
		"password" : "user3"
	}
]

# Class user with required methods.
class User():

	def __init__(self, mail):
		self.id = mail

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.id)

# Login form
class LoginForm(Form):
    mail = TextField('mail', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])

# This method checks if username and password are correct.
def check_credentials(email, password):
	for user in users_database:
		if user["mail"] == email and user["password"] == password:
			return True
	return False

#
@login_manager.user_loader
def load_user(userid):
	return  User(userid)

@app.route('/')
def hello_world():
    return render_template("public.html")

@app.route('/private')
@login_required
def serve_index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		mail = request.form["mail"] 
		password = request.form["password"]
		if check_credentials(mail, password):
			user = User(mail)
			login_user(user)
			return render_template("index.html")
		else:
			abort(401)
	return render_template("login.html", form = form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
