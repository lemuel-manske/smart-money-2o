from hmac import compare_digest
from app import db


class User(db.Model):
	__tablename__ = 'User'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	email = db.Column(db.Text, nullable=False)
	password = db.Column(db.Text, nullable=False)

	def toJson(self):
		return {
			'id' : self.id,
			'name' : self.name,
			'email' : self.email,
			'password' : self.password
		}

	def check_password(self, passwordToCheck: 'str'):
		return compare_digest(self.password, passwordToCheck)
	
	def __str__(self):
		return f'<User: id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}>'