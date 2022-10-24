from http.client import CONFLICT

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app, db
from app.models import ContaBancaria
from app.utils import get_validate
from app.utils.choices import Moedas, Instituicoes


@app.route('/home', methods=['GET'])
def home_route():
	'''
	Rota home/padrão.
	'''
	return '<h1>Home</h1>'


@app.route('/criar/conta-bancaria', methods=['POST'])
@jwt_required()
def create_bank_account_route():
	moeda, saldo, instituicao = get_validate(request.get_json(), 
	{'moeda': str,
	 'saldo': str,
	 'instituicao': str})

	id_usuario = get_jwt_identity()

	if not Moedas.has_name(moeda) or \
		not Instituicoes.has_name(instituicao):
			abort(CONFLICT) # TODO: codigo correto/ideal ?

	nova_conta_bancaria = ContaBancaria(
		moeda = Moedas[moeda],
		saldo = saldo,
		instituicao = Instituicoes[instituicao],
		id_usuario = id_usuario
	)

	db.session.add(nova_conta_bancaria)
	db.session.commit()

	return jsonify(nova_conta_bancaria.json()), 200