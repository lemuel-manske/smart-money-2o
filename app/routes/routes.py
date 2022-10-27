from http.client import CONFLICT, NOT_FOUND, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app, db
from app.models import ContaBancaria, Transacao
from app.utils import get_conta_bancaria, get_validate
from app.utils.choices import Moedas, Instituicoes, TipoTransacao


@app.route('/home', methods=['GET'])
def home_route():
	'''
	Rota home/padrão.
	'''
	return '<h1>Home</h1>'


@app.route('/criar/conta-bancaria', methods=['POST'])
@jwt_required()
def rota_criar_conta_bancaria():
	'''
	TODO
	'''
	moeda, saldo, instituicao = get_validate(request.get_json(), 
	{
		'moeda': str,
		'saldo': str,
		'instituicao': str
	})

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


@app.route('/criar/<tipo: str>', methods=['POST'])
@app.route('/criar/despesa', methods=['POST'])
def rota_criar_despesa():
	'''
	TODO
	'''
	valor, descricao, resolvido, id_categoria, id_conta_bancaria = \
		get_validate(request.get_json(),
	{
		'valor': str, 
		'descricao': str, 
		'resolvido': bool, 
		'id_categoria': int, 
		'id_conta_bancaria': int
	})

	id_usuario = get_jwt_identity()

	conta_bancaria = get_conta_bancaria(id_usuario, id_conta_bancaria)

	nova_despesa = Transacao(
		tipo = TipoTransacao.DESPESA,
		valor = valor,
		descricao = descricao,
		resolvido = resolvido,
		id_categoria = id_categoria,
		id_conta_bancaria = id_conta_bancaria,
	)

	db.session.add(nova_despesa)
	db.session.commit