from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask('SmartMoney')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Padrão None. Caso True requer processamento extra

app.config['SECRET_KEY'] = \
	b',`\xe2\x95\xe0\x84\xd0\x0c=8\x19\xdbU\xe2\xff\xdb&\xbc\x11\xf3\xdb\xd1\xabO\xac0\xd6\xd0}v\x8c\x10'
	
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)

db = SQLAlchemy(app)
db.session.execute('PRAGMA FOREIGN_KEYS=ON')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

TOKEN_UPDATE_HEADER = 'X-SM-Update-Bearer-Token'
# SM -> Smart Money

cors = CORS(app, expose_headers=[TOKEN_UPDATE_HEADER], allow_headers=['Authorization'])

from app.routes import auth
from app.routes import routes