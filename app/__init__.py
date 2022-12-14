from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config=Config):
	app = Flask('SmartMoney')
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)

	with app.app_context():
		# Habilitar chaves estrangeiras
		db.session.execute('PRAGMA FOREIGN_KEYS=ON')

	from app.api.auth import auth_routes
	from app.api.user import user_routes
	from app.api.create import create_routes
	from app.api.delete import delete_routes
	from app.api.list import list_routes

	from app.routes.auth import auth_render
	from app.routes.home import home_render
	from app.routes.main import main_render

	app.register_blueprint(auth_routes)
	app.register_blueprint(user_routes)
	app.register_blueprint(create_routes)
	app.register_blueprint(delete_routes)
	app.register_blueprint(list_routes)

	app.register_blueprint(auth_render)
	app.register_blueprint(home_render)
	app.register_blueprint(main_render)
	
	return app
