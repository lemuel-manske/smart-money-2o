from flask import Blueprint, render_template

from app.decorators import check_for_jwt


auth_render = Blueprint('auth_render', __name__, url_prefix='/auth')

@auth_render.get('/login')
def render_login():
	'''
	Rota de login.
	'''
	return render_template('login.html', title='Login')

@auth_render.get('/cadastro')
def render_cadastro():
	'''
	Rota de cadastro.
	'''
	return render_template('cadastro.html', title='Cadastro')

@auth_render.get('/minha-conta')
@check_for_jwt
def render_minha_conta():
	'''
	Rota "minha-conta".

	Serve como o perfil do usuário, e também
	página que o usário pode atualizar a senha e o nome.
	'''
	return render_template('minha_conta.html')