from enum import Enum
from http.client import BAD_REQUEST
from operator import itemgetter

from flask import abort

def get_validate(data: any, schema: 'dict[str, type]') -> 'dict[str, any]':

	if type(data) != dict:
		abort(BAD_REQUEST)

	for key in schema:
		if (key not in data) or (type(data[key]) != schema[key]):
			abort(BAD_REQUEST)

	return itemgetter(*schema)(data)

	
def enum_value_check(enum: Enum, value: str):
	try: 
		enum[value]
		
		return value
		
	except KeyError as err:
		return err.__name__, False
