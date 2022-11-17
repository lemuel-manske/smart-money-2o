from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

TOKEN_UPDATE_HEADER = 'X-SM-Update-Bearer-Token'

cors = CORS(expose_headers=[TOKEN_UPDATE_HEADER], allow_headers=['Authorization'])

def create_app(config=Config):
	app = Flask('SmartMoney')
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)
	cors.init_app(app)

	with app.app_context():
		db.session.execute('PRAGMA FOREIGN_KEYS=ON')

	from app.api.auth import auth_routes
	from app.api.create import create_routes
	from app.api.list import list_routes
	from app.api.home import home_routes

	app.register_blueprint(auth_routes)
	app.register_blueprint(create_routes)
	app.register_blueprint(home_routes)
	app.register_blueprint(list_routes)

	return app
