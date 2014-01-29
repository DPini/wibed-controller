from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import Required, ValidationError
from database import db
from models.user import User

class LoginForm(Form):
	name = TextField("Username", [Required("Please enter your email address.")])
	password = PasswordField('Password', [Required("Please enter a password.")])
	submit = SubmitField("Login")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
	
		user = User.query.filter_by( name = self.name.data).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.name.errors.append("Invalid username or password")
			return False
