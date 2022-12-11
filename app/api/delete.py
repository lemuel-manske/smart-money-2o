from flask import request, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import ContaBancaria, Transacao, Transferencia
from app.utils import get_validate, response


delete_routes = Blueprint('delete_routes', __name__, url_prefix='/api/delete')

@delete_routes.route('/conta-bancaria', methods=['DELETE'])
@jwt_required()
def rota_deletar_conta_bancaria():
	'''
	'''
	id_conta_bancaria = get_validate(request.get_json(), 
	{
		'id_conta_bancaria': int
	})

	conta_bancaria: ContaBancaria = ContaBancaria.query.filter_by(id=id_conta_bancaria).first()

	if conta_bancaria == None:
		return response(404, 'Nenhuma conta bancária encontrada')

	if conta_bancaria.id_usuario != get_jwt_identity():
		return response(401, 'Você não possui permissão para deletar essa conta bancária')

	db.session.delete(conta_bancaria)
	db.session.commit()

	return response(200, 'Conta bancária removida com sucesso')


@delete_routes.route('/transacao', methods=['DELETE'])
@jwt_required()
def rota_deletar_transacao():
	'''
	'''
	id_transacao = get_validate(request.get_json(), 
	{
		'id_transacao': int
	})

	transacao: Transacao = Transacao.query.filter_by(id=id_transacao).first()

	if transacao == None:
		return response(404, 'Nenhuma transação encontrada')

	if transacao.id_usuario != get_jwt_identity():
		return response(401, 'Você não possui permissão para deletar essa transação')

	transacao.excluir_transacao()

	db.session.delete(transacao)
	db.session.commit()

	return response(200, 'Transação removida com sucesso')


@delete_routes.route('/transferencia', methods=['DELETE'])
@jwt_required()
def rota_deletar_transferencia():
	'''
	'''
	id_transferencia = get_validate(request.get_json(), 
	{
		'id_transferencia': int
	})

	transferencia: Transferencia = Transferencia.query.filter_by(id=id_transferencia).first()

	if transferencia == None:
		return response(404, 'Nenhuma transferência encontrada')

	if transferencia.id_usuario != get_jwt_identity():
		return response(401, 'Você não possui permissão para deletar essa transferência')

	transferencia.excluir_transferencia()

	db.session.delete(transferencia)
	db.session.commit()

	return response(200, 'Transferêmcia removida com sucesso')
