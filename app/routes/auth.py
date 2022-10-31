from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app import TOKEN_UPDATE_HEADER, app, bcrypt
from app.models import Usuario
from app.utils import get_validate


@app.route('/login', methods=['POST'])
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
		return jsonify('Usuário não encontrado.'), 404

	if not bcrypt.check_password_hash(usuario.senha, senha):
		return jsonify('Senha incorreta.'), 409
	
	tk = create_access_token(identity=usuario.id)

	res = jsonify(usuario.json())
	res.headers.set(TOKEN_UPDATE_HEADER, tk)

	return res, 200
	

@app.route('/cadastro', methods=['POST'])
def rota_register():
	'''
	Realiza registro de um novo usuário via POST.

	Realiza request de dados em json (email, senha e nome),
	validando os mesmos (`get_validate`).

	Realiza o login imediatamente após confirmação de sucesso (JWT).

	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 409 (CONFLICT): Usuário já existe (filtro p/ email).
	'''
	email, senha, nome = get_validate(request.get_json(), \
		{
			'email': str,
			'senha': str,
			'nome': str
		})

	if Usuario.query.filter_by(email=email).first() != None:
		return jsonify('Email já cadastrado.'), 409
		
	senha_hash = bcrypt.generate_password_hash(senha).decode('UTF-8')

	novo_usuario: Usuario = Usuario.create(
		email=email,
		senha=senha_hash,
		nome=nome
	)

	tk = create_access_token(identity=novo_usuario.id)

	res = jsonify(novo_usuario.json())
	res.headers.set(TOKEN_UPDATE_HEADER, tk)

	return res, 200


@app.route('/atualizar-conta', methods=['POST'])
@jwt_required()
def rota_atualizar_conta():
	email, senha, senha_nova, nome = get_validate(request.get_json(), \
		{
			'email': str,
			'senha': str,
			'nova_senha': str,
			'nome': str
		})
	
	id_usuario = get_jwt_identity()

	usuario: Usuario = Usuario.query.filter_by(id=id_usuario).first()

	if not bcrypt.check_password_hash(usuario.senha, senha):
		return jsonify('Senha incorreta.'), 409

	nova_senha_hash = bcrypt.generate_password_hash(senha_nova).decode('UTF-8')

	usuario.update(
		email=email, 
		senha=nova_senha_hash,
		nome=nome
	)

	return jsonify(usuario.json()), 200


@app.route('/minha-conta', methods=['GET'])
@jwt_required()
def rota_account():
	'''
	Retorna os dados da conta do usuário com login na sessão.

	Returns:
		CÓD. 200 (OK): Retorno dos dados do usuário em
			formato json.
	'''
	id_usuario = get_jwt_identity()

	usuario: Usuario = Usuario.query.filter_by(id=id_usuario).first()
	
	return jsonify(usuario.json()), 200