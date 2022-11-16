import os
from app import create_app
from app import db


if __name__ == '__main__':
	app = create_app()

	with app.app_context():
		os.remove('database.db')
		db.create_all()