from ast import Return
from http.client import BAD_REQUEST
from operator import itemgetter

from flask import request, abort
from typing import TypeVar

T = TypeVar('T')

def get_validate(type: 'type[T]', *fields: str) -> 'tuple[T, ...]':
	data = request.get_json()

	if (type(fields) != dict):
		abort(BAD_REQUEST)

	for field in fields:
		if (field not in data) or (type(data[field]) != type):
			abort(BAD_REQUEST)
	
	return itemgetter(*fields)(data)
	

