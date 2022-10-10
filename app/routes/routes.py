from http.client import CONFLICT, NOT_FOUND, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token

from app import TOKEN_UPDATE_HEADER, app, db, bcrypt
from app.models import Usuario
from app.utils import get_validate

@app.route('/home', methods=['GET'])
def home_route():
	return '<h1>Home</h1>'


@app.route('/login', methods=['POST'])
def rota_login():
	email, senha = get_validate(request.get_json(), {'email': str, 'senha':str})

	usuario = Usuario.query.filter_by(email=email).first()

	if (usuario == None):
		abort(NOT_FOUND)

	if not usuario.senha == senha:
		abort(UNAUTHORIZED)
	
	#TODO: criar JWT

	return jsonify(usuario.json())


@app.route('/register', methods=['POST'])
def rota_register():
	email, senha, nome = get_validate(request.get_json(), \
		{'email': str,'senha': str,'nome': str})

	if Usuario.query.filter_by(email=email).first() != None:
		abort(CONFLICT)
		
	senha_hash = bcrypt.generate_password_hash(senha).decode('UTF-8')

	novo_usuario = Usuario(
		email=email,
		senha=senha_hash,
		nome=nome
	)

	db.session.add(novo_usuario)
	db.session.commit()

	tk = create_access_token(identity=novo_usuario.id)

	response = jsonify(novo_usuario.json())
	response.headers.set(TOKEN_UPDATE_HEADER, tk)

	return response


@app.route('/account', methods=['GET'])
def rota_account():	
	pass