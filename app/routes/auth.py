from flask import Blueprint, render_template

from app.decorators import check_for_jwt

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.get('/login')
def render_login():
	return render_template('login.html', title='Login')

@auth.get('/cadastro')
def render_cadastro():
	return render_template('cadastro.html', title='Cadastro')

@auth.get('/minha-conta')
@check_for_jwt
def render_minha_conta():
	return render_template('minha_conta.html')