from flask import Blueprint, request

from flask_jwt_extended import get_jwt_identity, jwt_required, unset_jwt_cookies

from app import bcrypt
from app.utils import get_validate, response, email_validate
from app.utils.choices import Moedas

from app.models import Usuario


user_routes = Blueprint('user_routes', __name__, url_prefix='/api/user')


@user_routes.post('/atualizar-conta')
@jwt_required()
def rota_atualizar_conta():
	'''
	Realiza a alteração dos dados do usuário via POST.

	Realiza request de dados em json (email, senha, nova_senha e nome),
	validando os mesmos (`get_validate`).

	Returns:
		CÓD. 200 (OK): Atualiza os dados e retorna objeto 
			usuário em formato json.
		CÓD. 400 (BAD REQUEST): Email inválido com base em regex.
		CÓD. 401 (UNAUTHORIZED): Senha incorreta.
	'''
	senha, senha_nova, nome, moeda = get_validate(request.get_json(), \
		{
			'senha': str,
			'nova_senha': str,
			'nome': str,
			'moeda': str
		})
	
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	if not Moedas.has_name(moeda.upper()):
		return response(401, 'O tipo de moeda informada não corresponde a algum presente em nosso sistema')

	if not bcrypt.check_password_hash(usuario.senha, senha):
		return response(401, 'Senha incorreta', 'senha')

	nova_senha_hash = bcrypt.generate_password_hash(senha_nova).decode('UTF-8')

	usuario.update(
		senha=nova_senha_hash,
		nome=nome,
		moeda = Moedas[moeda.upper()],
	)

	res = response(200, usuario.json())

	return res


@user_routes.get('/logout')
@jwt_required()
def rota_logout():
	'''
	Realiza o logout do usuário.

	Returns:
		CÓD. 200 (OK): JWT excluída.
	'''
	resp = response(200, 'Logout bem sucedido')
	unset_jwt_cookies(resp)

	return resp


@user_routes.get('/minha-conta')
@jwt_required()
def rota_minha_conta():
	'''
	Retorna as informações do usuário

	Returns:
		CÓD. 200 (OK): Objeto json com informações 
			da conta do usuário
	'''
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	resp = response(200, usuario.json())

	return resp
