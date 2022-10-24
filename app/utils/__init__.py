from http.client import BAD_REQUEST

from enum import Enum

from operator import itemgetter

from flask import abort


def get_validate(data: any, schema: 'dict[str, type]') -> 'dict[str, any]':

	if type(data) != dict:
		abort(BAD_REQUEST)

	for key in schema:
		if (key not in data) or (type(data[key]) != schema[key]):
			abort(BAD_REQUEST)

	return itemgetter(*schema)(data)