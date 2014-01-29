from database import db
from werkzeug import generate_password_hash, check_password_hash

class User(db.Model):
	"""
	Represents a User
	"""
	
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	pwdhash = db.Column(db.String(54))

	def __init__(self, name, password):
		self.name = name
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.pwdhash, password)

	def is_admin(self):
		if self.name == "admin":
			return True
		return False

