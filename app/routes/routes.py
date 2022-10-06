from http.client import NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, jsonify

from flask_jwt_extended import create_access_token

from app import app, db, bcrypt, TOKEN_UPDATE_HEADER
from app.models import ContaBancaria, Usuario
from app.utils import get_validate
from app.utils.choices import Instituicoes, Moedas

@app.route('/home', methods=['GET'])
def home_route():
	return '<h1>Home</h1>'


@app.route('/login', methods=['POST'])
def rota_login():
	email, senha = get_validate(str, 'email', 'senha')

	usuario = Usuario.query.filter_by(email=email).first()

	if (usuario == None):
		abort(NOT_FOUND)

	if not usuario.senha == senha:
		abort(UNAUTHORIZED)
	
	# token = create_access_token(identity=usuario.id)
		
	response = jsonify(usuario.json())
	# response.headers.set(TOKEN_UPDATE_HEADER, token)

	return response


@app.route('/teste')
def teste_db():
	user = Usuario(
		nome='lemuel',
		email='lemuelkaue@gmail.com',
		senha='123'
	)

	db.session.add(user)
	db.session.commit()

	conta_bancaria = ContaBancaria(
		moeda=Moedas.BRAZIL,
		saldo=800,
		instituicao=Instituicoes.NUBANK,
		id_usuario=1
	)

	db.session.add(conta_bancaria)
	db.session.commit()

	return user.json()