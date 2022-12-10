from datetime import timedelta

class Config():
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False # Padrão None. Caso True requer processamento extra
	JWT_SECRET_KEY = b',`\xe2\x95\xe0\x84\xd0\x0c=8\x19\xdbU\xe2\xff\xdb&\xbc\x11\xf3\xdb\xd1\xabO\xac0\xd6\xd0}v\x8c\x10'
	JWT_TOKEN_LOCATION = ['cookies']
	JWT_COOKIE_SECURE = False
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)