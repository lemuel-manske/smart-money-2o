from http.client import BAD_REQUEST, NOT_FOUND

from operator import itemgetter

from flask import abort

from app.models import ContaBancaria

def get_validate(data: any, schema: 'dict[str, type]') -> 'dict[str, any]':

	if type(data) != dict:
		abort(BAD_REQUEST)

	for key in schema:
		if (key not in data) or (type(data[key]) != schema[key]):
			abort(BAD_REQUEST) # 401

	return itemgetter(*schema)(data)


def get_conta_bancaria(b_id: int, u_id: int):
	c = ContaBancaria.query.filter_by(id=b_id, id_usuario=u_id)
	
	if not c:
		abort(NOT_FOUND)

	return c