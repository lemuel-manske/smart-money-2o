from flask import request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Categoria, ContaBancaria, Transacao, Transferencia
from app.utils import get_validate, response
from app.utils.enums import Instituicoes, TipoTransacao


create_routes = Blueprint('create_routes', __name__, url_prefix='/api/create')

@create_routes.post('/conta-bancaria')
@jwt_required()
def rota_criar_conta_bancaria():
	'''
	Realiza a criação de uma nova conta bancária na conta do usuário.

	Args:
		nome: str;
		saldo: str;
		instituicao: str.

	Para instituição bancária é realizado verificação de compatibilidade
	com os tipos presentes na classe enumeradora `Instituicao`
	(`choices.py`).

	Returns:
		CÓD. 200 (OK): Cadastro da conta bancária e retorno dos dados 
			cadastrados em formato json.
		CÓD 404 (NOT_FOUND): Instituição bancária informada não 
			compatível com os valores presentes no enumerador.
	'''
	nome, saldo, instituicao = get_validate(request.get_json(), 
	{
		'nome': str,
		'saldo': str,
		'instituicao': str
	})

	if 	not Instituicoes.possui(instituicao.upper()):
		return response(404, 'Nome de instituição informada não existente. Consulte /enum/instituicao')

	nova_conta_bancaria: ContaBancaria = ContaBancaria.criar_instancia(
		nome = nome,
		saldo = saldo,
		instituicao = Instituicoes[instituicao.upper()],
		id_usuario = get_jwt_identity()
	)

	return response(200, nova_conta_bancaria.json())


@create_routes.post('/transacao/<string:tipo>')
@jwt_required()
def rota_criar_transacao(tipo:str = 'despesa'):
	'''
	Realiza o cadastro de uma nova transação na conta do usuário.

	Args:
		valor: str;
		descricao: str;
		resolvido: bool;
		id_categoria: int;
		id_conta_bancaria: int.

	Para o parâmetro `tipo` na URL, é realizado verificação de 
	correspondência com os valores presentes na classe
	enumeradora `TipoTransacao`.

	O id de categoria informado deve corresponder ao mesmo tipo informado por
	URL, isto é, 'despesa' para ambos ou 'receita' para ambos.

	Returns:
		CÓD. 200 (OK): Cadastro de nova transação e retorno dos dados 
			cadastrados em formato json;
		CÓD 401 (UNAUTHORIZED): O id da categoria informado não corresponde, ou
			parâmetro na URL não corresponde a nenhum valor na classe `TipoTransacao`;
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
		return response(404, 'Nenhuma conta bancária ou categoria com o id informado \
			foi encontrada. Consulte /listar/<nome-da-classe>')

	if categoria.tipo.name != tipo.upper():
		return response(401, f'O id de categoria informado não corresponde a {tipo}')

	if not TipoTransacao.possui(tipo.upper()):
		return response(401, 'O tipo de transação informada não corresponde a `despesa` ou `receita`')

	nova_transacao: Transacao = Transacao.criar_instancia(
		tipo = TipoTransacao[tipo.upper()],
		valor = valor,
		descricao = descricao,
		resolvido = resolvido,
		id_categoria = id_categoria,
		id_usuario = id_usuario,
		id_conta_bancaria = id_conta_bancaria,
	)

	nova_transacao.realizar_transacao()

	return response(200, nova_transacao.json())


@create_routes.post('/transacao/realizar')
@jwt_required()
def rota_realizar_transacao():
	'''
	Realiza a efetuação de uma transação, isto é, a transação
	é tida como paga ou recebida e o saldo da conta bancária
	associada é reavido.

	Args:
		id_transacao: int.

	Returns:
		CÓD. 200 (OK): Cadastro da categoria e retorno dos dados 
			cadastrados em formato json;
		CÓD 401 (UNAUTHORIZED): Usuário não possui permissão para
			efetuar a transação;
		CÓD 404 (NOT_FOUND): Transação com id informado não foi
			encontrada.
	'''
	id_transacao = get_validate(request.get_json(), 
	{
		'id_transacao': int
	})

	transacao: Transacao = Transacao.query.filter_by(id=id_transacao).first()

	if transacao == None:
		return response(404, 'Nenhuma transação encontrada')

	if transacao.id_usuario != get_jwt_identity():
		return response(401, 'Você não possui permissão para modificar essa transação')

	transacao.atualizar_instancia(
		resolvido = True
	)
	db.session.commit()

	transacao.realizar_transacao()

	return response(200, 'Transação foi resolvida')


@create_routes.post('/categoria/<string:tipo>')
@jwt_required()
def rota_criar_categoria(tipo:str):
	'''
	Realiza o cadastro de uma nova categoria na conta do usuário.

	Args:
		nome: str;
		icone: str.

	Para o tipo de categoria (informado p/ URL) verificação de 'compatibilidade'
	com os tipos presentes na classe enumeradora `TipoTransacao` 
	(choices.py).

	Returns:
		CÓD. 200 (OK): Cadastro da categoria e retorno dos dados 
			cadastrados em formato json;
		CÓD 401 (UNAUTHORIZED): Tipo de categoria informado não 
			compatível com 'despesa' ou 'receita'.
	'''
	nome, icone = get_validate(request.get_json(), 
	{
		'nome': str,
		'icone': str
	})

	if not TipoTransacao.possui(tipo.upper()):
		return response(401, 'O tipo de categoria informada por URL não corresponde a `despesa` ou `receita`')

	nova_categoria: Categoria = Categoria.criar_instancia(
		tipo = TipoTransacao[tipo.upper()],
		nome = nome,
		icone = icone,
		id_usuario = get_jwt_identity()
	)

	return response(200, nova_categoria.json())


@create_routes.post('/transferencia')
@jwt_required()
def rota_criar_transferencia():
	'''
	Realiza o cadastro de uma nova transferência
	entre contas bancárias na conta do usuário.

	Args:
		valor: str;
		id_conta_bancaria_origem: int;
		id_conta_bancaria_destino: int.
	
	Returns:
		CÓD. 200 (OK): Criação da transferência e retorno dos dados 
			cadastrados em formato json;
		CÓD 400 (BAD_REQUEST): A conta bancária de origem deve ser
			diferente da conta bancária de destino;
		CÓD 401 (UNAUTHORIZED): O usuário da sessão atual não possui
			acesso a conta bancária de origem ou destino.
	'''
	valor, id_conta_bancaria_origem, id_conta_bancaria_destino = get_validate(request.get_json(), 
	{
		'valor': str,
		'id_conta_bancaria_origem': int,
		'id_conta_bancaria_destino': int
	})

	id_usuario = get_jwt_identity()

	conta_bancaria_destino = ContaBancaria.query \
		.filter_by(id=id_conta_bancaria_destino, id_usuario=id_usuario).first() 
	
	conta_bancaria_origem = ContaBancaria.query \
		.filter_by(id=id_conta_bancaria_origem, id_usuario=id_usuario).first() 

	if (conta_bancaria_destino == None or conta_bancaria_origem == None):
		return response(401, 'Você não possui acesso a essa conta bancária')

	if (conta_bancaria_destino.id == conta_bancaria_origem.id):
		return response(400, 'A conta de destino deve ser diferente da conta de origem', 'contas_bancarias_destino_select')

	nova_transferencia: Transferencia = Transferencia.criar_instancia(
		valor = valor,
		id_usuario = id_usuario,
		id_conta_bancaria_origem = id_conta_bancaria_origem,
		id_conta_bancaria_destino = id_conta_bancaria_destino
	)

	nova_transferencia.realizar_transferencia(conta_bancaria_origem, conta_bancaria_destino)

	return response(200, nova_transferencia.json())
