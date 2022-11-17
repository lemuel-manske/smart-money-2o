from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Categoria, ContaBancaria, Transacao
from app.utils import get_validate, return_error
from app.utils.choices import Moedas, Instituicoes, TipoTransacao


create_routes = Blueprint('create_routes', __name__, url_prefix='/api/create')

@create_routes.route('/conta-bancaria', methods=['POST'])
@jwt_required()
def rota_criar_conta_bancaria():
	'''
	Realiza o cadastro de uma nova conta bancária 
	na conta do usuário via POST.

	Realiza request de dados em json (tipo de moeda, saldo e instituição
	bancária), validando os mesmos (`get_validate`).

	Para moeda e instituição é realizado verificação de 'compatibilidade'
	com os tipos presentes em classes enumeradoras `Moeda` e `Instituicao` 
	(`choices.py`).

	Returns:
		CÓD. 200 (OK): Cadastro da conta bancária e retorno dos dados 
			cadastrados em formato json.
		CÓD 404 (NOT_FOUND): Moeda ou instituição bancária informada não 
			compatíveis com os valores presentes nos enumeradores.
	'''
	moeda, saldo, instituicao = get_validate(request.get_json(), 
	{
		'moeda': str,
		'saldo': str,
		'instituicao': str
	})

	id_usuario = get_jwt_identity()

	if not Moedas.has_name(moeda.upper()) or \
		not Instituicoes.has_name(instituicao.upper()):
			return_error(400, 'Nome de moeda ou instituição informada não existente. Consulte /enum.')

	nova_conta_bancaria: ContaBancaria = ContaBancaria.create(
		moeda = Moedas[moeda.upper()],
		saldo = saldo,
		instituicao = Instituicoes[instituicao.upper()],
		id_usuario = id_usuario
	)

	return jsonify(nova_conta_bancaria.json()), 200


@create_routes.route('/transacao/<string:tipo>', methods=['POST'])
@jwt_required()
def rota_criar_transacao(tipo:str = 'despesa'):
	'''
	Realiza o cadastro de uma nova transação 
	na conta do usuário via POST.

	Realiza request de dados em json (valor, descrição, resolvido, 
	id_categoria e id_conta_bancaria), validando os mesmos (`get_validate`).

	Para o parâmetro `tipo` na URL, é realizado verificação de 
	correspondência com os valores presentes na classe
	enumeradora `TipoTransacao`.

	O id de categoria informado deve corresponder ao mesmo tipo informado por
	URL, isto é, 'despesa' para ambos ou 'receita' para ambos.

	Returns:
		CÓD. 200 (OK): Cadastro de nova transação e retorno dos dados 
			cadastrados em formato json.
		CÓD 401 (UNAUTHORIZED): O id da categoria informado não corresponde;
			parâmetro na URL não corresponde a nenhum valor na classe `TipoTransacao`
		CÓD 404 (NOT_FOUND): Nenhuma conta bancária ou categoria com o 
			id informado foi encontrada.
	'''
	valor, descricao, resolvido, id_categoria, id_conta_bancaria = get_validate(request.get_json(), 
	{
		'valor': str, 
		'descricao': str, 
		'resolvido': bool, 
		'id_categoria': int, 
		'id_conta_bancaria': int
	})

	id_usuario = get_jwt_identity()

	conta_bancaria = ContaBancaria.query \
		.filter_by(id=id_conta_bancaria, id_usuario=id_usuario).first()

	categoria = Categoria.query \
		.filter_by(id=id_categoria, id_usuario=id_usuario).first()

	if conta_bancaria == None or categoria == None:
		return_error(404, 'Nenhuma conta bancária ou categoria com o id informado \
			foi encontrada. Consulte /listar/<nome_classe>.')

	if categoria.tipo.name != tipo.upper():
		return_error(401, f'O id de categoria informado não corresponde a {tipo}')

	if not TipoTransacao.has_name(tipo.upper()):
		return_error(401, 'O tipo de transação informada por URL não corresponde a `despesa` ou `receita`')

	nova_transacao: Transacao = Transacao.create(
		tipo = TipoTransacao[tipo.upper()],
		valor = valor,
		descricao = descricao,
		resolvido = resolvido,
		id_categoria = id_categoria,
		id_usuario=id_usuario,
		id_conta_bancaria = id_conta_bancaria,
	)

	nova_transacao.do_transacao(conta_bancaria=conta_bancaria)

	return jsonify(nova_transacao.json()), 200


@create_routes.route('/categoria/<string:tipo>', methods=['POST'])
@jwt_required()
def rota_criar_categoria(tipo:str):
	'''
	Realiza o cadastro de uma nova categoria 
	na conta do usuário via POST.

	Realiza request de dados em json (nome e ícone), validando os 
	mesmos (`get_validate`).

	Para o tipo de categoria verificação de 'compatibilidade'
	com os tipos presentes na classe enumeradora `TipoTransacao` 
	(choices.py).

	Returns:
		CÓD. 200 (OK): Cadastro da categoria e retorno dos dados 
			cadastrados em formato json.
		CÓD 401 (BAD_REQUEST): Tipo de categoria informado não 
			compatível com 'despesa' ou 'receita'.
	'''
	nome, icone = get_validate(request.get_json(), 
	{
		'nome': str,
		'icone': str
	})

	id_usuario = get_jwt_identity()

	if not TipoTransacao.has_name(tipo.upper()):
		return_error(401, 'O tipo de categoria informada por URL não corresponde a `despesa` ou `receita`')

	nova_categoria: Categoria = Categoria.create(
		tipo = TipoTransacao[tipo.upper()],
		nome = nome,
		icone = icone,
		id_usuario = id_usuario
	)

	return jsonify(nova_categoria.json()), 200