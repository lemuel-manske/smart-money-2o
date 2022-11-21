from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import Usuario
from app.utils import return_error


list_routes = Blueprint('list_routes', __name__, url_prefix='/api/list')

@list_routes.route('/<string:classe>', methods=['GET'])
@jwt_required()
def rota_listar(classe):
	'''
	Rota de listagem genérica.

	Extrai a nome da classe através do URL e retorna as
	informações contempladas pela conta do usuário na 
	sessão (JWT necessário).

	Returns:
		CÓD. 200 (OK): Retorno de informações em formato json.
		CÓD 404 (NOT_FOUND): Nome da classe informada não contempla
			nenhum modelo do banco de dados.
	'''	
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	resultado = None

	if classe == 'contas-bancarias':
		resultado = usuario.contas_bancarias
	elif classe == 'transacoes':
		resultado = usuario.transacoes
	elif classe == 'categorias':
		resultado = usuario.categorias
	else:	
		return_error(404, 'Nenhuma classe encontrada com o nome informado.')

	resp = [ instance.json() for instance in resultado ]

	return jsonify(resp)