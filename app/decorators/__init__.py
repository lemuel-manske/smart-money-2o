from functools import wraps

from flask import redirect, url_for
from flask_jwt_extended import verify_jwt_in_request
 

def check_for_jwt(route):
	'''
	Realiza verificação de JWT no request,
	com `optional=True`, isso significa que 
	caso uma JWT seja encontrada o retorno é True,
	caso contrário o retorno é None.

	Caso nenhuma JWT seja encontrada, a função
	redireciona o usuário para a página de login.
	'''
	@wraps(route)
	def wrapper(*args, **kwargs):
		if verify_jwt_in_request(optional=True) == None:
			return redirect(url_for('auth.render_login'))
		
		return route(*args, **kwargs)

	return wrapper
