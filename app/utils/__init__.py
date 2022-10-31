from http.client import BAD_REQUEST

from operator import itemgetter

from flask import abort

from app import db

def get_validate(data: any, schema: 'dict[str, type]') -> 'dict[str, any]':
	'''
	Realiza a verificação de campos via `request.get_json()`, comparando 
	se os campos desejados conforme schema são os mesmos que estão vindos por request.

	Returns:
		CÓD. 400 (BAD_REQUEST): Campos inválidos.
		Sucesso: Ordenação de campos vindos por request (itemgetter).
	'''

	if type(data) != dict:
		abort(BAD_REQUEST)

	for key in schema:
		if (key not in data) or (type(data[key]) != schema[key]):
			abort(BAD_REQUEST)

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