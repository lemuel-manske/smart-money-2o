import re

from operator import itemgetter

from flask import abort, jsonify

from app import db


EMAIL_REG_EX = re.compile("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

def response(status_code: int, message: str, target: str = None):
	if target == None:
		res = jsonify({
			'msg' : message,
		})
	else:
		res = jsonify({
			'msg' : message,
			'target' : target,
		})
	res.status_code = status_code

	return res

def get_validate(data: any, schema: 'dict[str, type]') -> 'dict[str, any]':
	'''
	Realiza a verificação de campos via `request.get_json()`, comparando 
	se os campos desejados conforme schema são os mesmos que estão vindos por request.

	Returns:
		CÓD. 400 (BAD_REQUEST): Campos inválidos.
		Sucesso: Ordenação de campos vindos por request (`itemgetter`).
	'''
	if type(data) != dict:
		response(400, 'Informe os dados em formato json {...}')

	for key in schema:
		if (key not in data) or (type(data[key]) != schema[key]):
			response(400, 'Campos inválidos. Consulte documentação.')

	return itemgetter(*schema)(data)

def do_add_commit(inst: db.Model):
	'''
	Realiza a adição de instancia de objeto (modelo)
	ao banco de dados, seguido de commit.

	db.session.add(inst)
	db.session.commit()
	'''
	db.session.add(inst)
	db.session.commit()

def email_validate(email):
	'''
	Realiza a verificação de email com base em regular 
	expression (EMAIL_REG_EX).
	'''
	return True if re.match(EMAIL_REG_EX, email) else False