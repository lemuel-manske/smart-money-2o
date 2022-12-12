from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Usuario
from app.utils import response


list_routes = Blueprint('list_routes', __name__, url_prefix='/api/list')

@list_routes.get('/<string:classe>')
@jwt_required()
def rota_listar(classe):
	'''
	Rota de listagem genérica.

	Extrai a nome da classe através do URL e retorna as
	informações contempladas pela conta do usuário na 
	sessão (JWT necessário).

	Returns:
		CÓD. 200 (OK): Retorno de informações em formato json;
		CÓD. 404 (NOT_FOUND): Nome da classe informada não contempla
			nenhum modelo do banco de dados.
	'''
	classes = {
		'contas-bancarias': usuario.contas_bancarias,
		'transacoes': usuario.transacoes,
		'categorias': usuario.categorias,
		'transferencias': usuario.transferencias,
	}
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	if classe in classes.keys():
		return response(200, [ instance.json() for instance in classes[classe] ])

	return response(404, 'Nenhuma classe encontrada com o nome informado')