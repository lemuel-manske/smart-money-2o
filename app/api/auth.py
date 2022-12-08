from flask import request, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies

from app import TOKEN_UPDATE_HEADER, bcrypt
from app.models import Categoria, ContaBancaria, Usuario
from app.utils import get_validate, response, email_validate
from app.utils.choices import Instituicoes, TipoTransacao


auth_routes = Blueprint('auth_routes', __name__, url_prefix='/api/auth')


# Vestuário
# Saúde
# Mercado
# Entretenimento
# Transporte 
# Educação

categorias_padroes = [
	{
		'tipo': 'DESPESA',
		'icone': 'vest',
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
	res.headers.set(TOKEN_UPDATE_HEADER, tk)

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
	res.headers.set(TOKEN_UPDATE_HEADER, tk)

	return res


@auth_routes.post('/atualizar-conta')
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
	email, senha, senha_nova, nome = get_validate(request.get_json(), \
		{
			'email': str,
			'senha': str,
			'nova_senha': str,
			'nome': str
		})
	
	usuario: Usuario = Usuario.query.filter_by(id=get_jwt_identity()).first()

	if not bcrypt.check_password_hash(usuario.senha, senha):
		response(401, 'Senha incorreta.')

	if not email_validate(email):
		response(400, 'Email inválido')

	nova_senha_hash = bcrypt.generate_password_hash(senha_nova).decode('UTF-8')

	usuario.update(
		email=email, 
		senha=nova_senha_hash,
		nome=nome
	)

	res = response(200, usuario.json())

	return res


@auth_routes.get('/logout')
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


@auth_routes.get('/minha-conta')
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
