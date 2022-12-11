from datetime import datetime, timedelta, timezone

from flask import Response, Blueprint, request

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies

from app import bcrypt
from app.utils import get_validate, response, email_validate
from app.utils.choices import Instituicoes, TipoTransacao

from app.models import Categoria, ContaBancaria, Usuario


auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api/auth')


categorias_padroes = [
	{
		'tipo': 'DESPESA',
		'icone': 'shirt',
		'nome': 'Vestuário',
	},
	{
		'tipo': 'DESPESA',
		'icone': 'hospital',
		'nome': 'Saúde',
	},
	{
		'tipo': 'DESPESA',
		'icone': 'market',
		'nome': 'Mercado',
	},
	{
		'tipo': 'DESPESA',
		'icone': 'entertainment',
		'nome': 'Entretenimento',
	},
	{
		'tipo': 'DESPESA',
		'icone': 'transport',
		'nome': 'Transporte',
	},
	{
		'tipo': 'DESPESA',
		'icone': 'education',
		'nome': 'Educação',
	},	
	{
		'tipo': 'RECEITA',
		'icone': 'gift',
		'nome': 'Presente',
	},
	{
		'tipo': 'RECEITA',
		'icone': 'cash',
		'nome': 'Salário',
	},

]


@auth_routes.post('/login')
def rota_login():
	'''
	Realiza o login do usuário via POST.

	Realiza request de dados em json (email e senha), 
	validando os mesmos (`get_validade`).

	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 401 (UNAUTHORIZED): Senha incorreta.
		CÓD. 404 (NOT_FOUND): Usuário não encontrado 
			no banco de dados.
	'''
	email, senha = get_validate(request.get_json(),
		{
			'email': str, 
			'senha':str
		})

	usuario: Usuario = Usuario.query.filter_by(email=email).first()

	if usuario == None:
		return response(404, 'Usuário não encontrado', 'email')

	if not bcrypt.check_password_hash(usuario.senha, senha):
		return response(401, 'Senha incorreta', 'senha')
	
	tk = create_access_token(identity=usuario.id)

	res = response(200, tk)
	
	set_access_cookies(res, tk)

	return res
	

@auth_routes.post('/cadastro')
def rota_cadastro():
	'''
	Realiza registro de um novo usuário via POST.

	Realiza request de dados em json (email, senha e nome),
	validando os mesmos (`get_validate`).

	Realiza o login imediatamente após confirmação de sucesso (JWT).

	Realiza a adição de categorias padrão na conta do usuário.

	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 400 (BAD REQUEST): Email inválido com base em regex.
		CÓD. 409 (CONFLICT): Usuário já existe (filtro p/ email).
	'''
	email, senha, nome = get_validate(request.get_json(), \
		{
			'email': str,
			'senha': str,
			'nome': str
		})

	if Usuario.query.filter_by(email=email).first() != None:
		return response(409, 'Email já cadastrado', 'email')

	if not email_validate(email):
		return response(400, 'Email inválido', 'email')
	
	senha_hash = bcrypt.generate_password_hash(senha).decode('UTF-8')

	novo_usuario: Usuario = Usuario.create(
		email = email,
		senha = senha_hash,
		nome = nome
	)

	for categoria in categorias_padroes:
		Categoria.create(
			tipo = TipoTransacao[categoria['tipo']],
			nome = categoria['nome'],
			icone = categoria['icone'],
			id_usuario = novo_usuario.id
		)
	
	ContaBancaria.create(
		nome = 'Carteira',
		saldo = 0,
		instituicao = Instituicoes['CARTEIRA'],
		id_usuario = novo_usuario.id
	)

	tk = create_access_token(identity=novo_usuario.id)

	res = response(200, tk)
	
	set_access_cookies(res, tk)

	return res


@auth_routes.after_app_request
def refresh_jwt_token(response: Response):
	try:
		expire_timestamp = get_jwt()['exp']
		now = datetime.now(timezone.utc)
		target_timestamp = datetime.timestamp(now + timedelta(minutes=30))

		if target_timestamp > expire_timestamp:
			token = create_access_token(get_jwt_identity())
			set_access_cookies(response, token)

		return response
	except (RuntimeError, KeyError):
		return response
