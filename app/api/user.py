from flask import Blueprint, request

from flask_jwt_extended import get_jwt_identity, jwt_required, unset_jwt_cookies

from app import bcrypt
from app.utils import get_validate, response, email_validate
from app.utils.enums import Moedas

from app.models import Usuario


user_routes = Blueprint('user_routes', __name__, url_prefix='/api/user')

@user_routes.post('/atualizar-conta')
@jwt_required()
def rota_atualizar_conta():
	'''
	Realiza a alteração dos dados do usuário.

	Args:
		senha: str;
		nova_senha: str;
		nome: str;
		moeda: str.

	Returns:
		CÓD. 200 (OK): Atualiza os dados e retorna objeto 
			usuário em formato json;
		CÓD. 401 (UNAUTHORIZED): Senha incorreta;
		CÓD. 404 (NOT_FOUND): Moeda informada não corresponde ao Enum Moedas.
	'''
	senha, nova_senha, nome, moeda = get_validate(request.get_json(), \
		{
			'senha': str,
			'nova_senha': str,
			'nome': str,
			'moeda': str
		})
	
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	if not Moedas.possui(moeda.upper()):
		return response(404, 'O tipo de moeda informada não corresponde a algum presente em nosso sistema')

	if not bcrypt.check_password_hash(usuario.senha, senha):
		return response(401, 'Senha incorreta', 'senha')

	nova_senha_hash = bcrypt.generate_password_hash(nova_senha).decode('UTF-8')

	usuario.atualizar_instancia(
		nome=nome,
		senha=nova_senha_hash,
		moeda = Moedas[moeda.upper()],
	)

	return response(200, usuario.json())


@user_routes.post('/logout')
@jwt_required()
def rota_logout():
	'''
	Realiza o logout do usuário, excluindo
	JWT existente.

	Returns:
		CÓD. 200 (OK): JWT excluída dos cookies.
	'''
	res = response(200, 'Logout bem sucedido')
	unset_jwt_cookies(res)

	return res


@user_routes.get('/minha-conta')
@jwt_required()
def rota_minha_conta():
	'''
	Retorna as informações do usuário em formato json.

	Returns:
		CÓD. 200 (OK): Objeto json com informações
			da conta do usuário
	'''
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	return response(200, usuario.json())
