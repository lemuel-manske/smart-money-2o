from http.client import BAD_REQUEST
from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app, db
from app.models import ContaBancaria
from app.utils import enum_value_check, get_validate
from app.utils.choices import Moedas, Instituicoes

@app.route('/home', methods=['GET'])
def home_route():
	'''
	Rota home/padrão.
	'''
	return '<h1>Home</h1>'

@app.route('/create/bank_account', methods=['POST'])
@jwt_required()
def create_bank_account_route():
	moeda, saldo, instituicao = get_validate(request.get_json(), 
	{'moeda': str,
	 'saldo': float,
	 'instituicao': str})

	curr_user = get_jwt_identity()

	if not enum_value_check(Moedas, moeda) and \
		not enum_value_check(Instituicoes, instituicao):
			abort(BAD_REQUEST)

	new_bank_account = ContaBancaria(
		moeda = Moedas[moeda],
		saldo = saldo,
		instituicao = Instituicoes[instituicao],
		id_usuario = curr_user
	)

	db.session.add(new_bank_account)
	db.session.commit()

	print(new_bank_account.json())	
	return '200', 200

# TODO: criacao de conta bancaria