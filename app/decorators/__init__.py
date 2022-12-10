from functools import wraps

from flask import redirect, url_for
from flask_jwt_extended import jwt_required, verify_jwt_in_request

from app.models import Usuario


def requer_login(route):
	@wraps(route)
	def wrapper(*args, **kwargs):
		if verify_jwt_in_request(optional=True) == None:
			return redirect(url_for('auth.render_login'))
		
		return route(*args, **kwargs)

	return wrapper
