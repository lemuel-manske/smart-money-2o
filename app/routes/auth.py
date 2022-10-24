from http.client import CONFLICT, NOT_FOUND, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app import TOKEN_UPDATE_HEADER, app, db, bcrypt
from app.models import Usuario
from app.utils import get_validate


@app.route('/login', methods=['POST'])
def rota_login():
	'''
	Realiza o login do usuário via POST.

	Realiza request de dados em json (email e senha), 
	validando os mesmos (get_validade).

	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 401 (UNAUTHORIZED): senha incorreta.
		CÓD. 404 (NOT_FOUND): usuário não encontrado 
			no banco de dados.
	'''
	email, senha = get_validate(request.get_json(),
		{'email': str, 
		 'senha':str})

	usuario = Usuario.query.filter_by(email=email).first()

	if (usuario == None):
		abort(NOT_FOUND)

	if not bcrypt.check_password_hash(usuario.senha, senha):
		abort(UNAUTHORIZED)
	
	tk = create_access_token(identity=usuario.id)

	response = jsonify(usuario.json())
	response.headers.set(TOKEN_UPDATE_HEADER, tk)

	return response, 200
	

@app.route('/cadastro', methods=['POST'])
def rota_register():
	'''
	Realiza registro de um novo usuário via POST.

	Realiza request de dados em json (email, senha e nome),
	validando os mesmos (get_validate).

	Realiza o login imediatamente após confirmação de sucesso (JWT).

	Returns:
		CÓD. 200 (OK): Criação de JWT (identidade id) e 
			retorna objeto usuário em formato json.
		CÓD. 409 (CONFLICT): Usuário já existe (filtro p/ email).
	'''
	email, senha, nome = get_validate(request.get_json(), \
		{'email': str,
		 'senha': str,
		 'nome': str})

	if Usuario.query.filter_by(email=email).first() != None:
		abort(CONFLICT)
		
	senha_hash = bcrypt.generate_password_hash(senha).decode('UTF-8')

	novo_usuario = Usuario(
		email=email,
		senha=senha_hash,
		nome=nome
	)

	db.session.add(novo_usuario)
	db.session.commit()

	tk = create_access_token(identity=novo_usuario.id)

	res = jsonify(novo_usuario.json())
	res.headers.set(TOKEN_UPDATE_HEADER, tk)

	return res, 200


@app.route('/minha-conta', methods=['GET'])
@jwt_required()
def rota_account():	
	current_user_id = get_jwt_identity()
	curr_user = Usuario.query.filter_by(id=current_user_id).first()
	
	return jsonify(curr_user.json()), 200
