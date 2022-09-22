from datetime import timedelta
from typing import TYPE_CHECKING

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

if TYPE_CHECKING:
	from typings import db_type_proxy
	db: db_type_proxy.SQLAlchemy

app = Flask('SmartMoney')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMT_TRACK_MODIFICATIONS'] = False # Padrão None. Caso True requer memória extra

app.config['SECRET_KEY'] = \
	b',`\xe2\x95\xe0\x84\xd0\x0c=8\x19\xdbU\xe2\xff\xdb&\xbc\x11\xf3\xdb\xd1\xabO\xac0\xd6\xd0}v\x8c\x10'
	
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
jwt = JWTManager(app)


import routes

if __name__ == '__main__':
	app.run(debug=True)