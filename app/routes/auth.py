from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.get('/login')
def render_login():
	return render_template('login.html')

@auth.get('/cadastro')
def render_cadastro():
	return render_template('cadastro.html')

@auth.get('/atualizar-conta')
def render_atualizar_conta():
	return render_template('atualizar_conta.html')

@auth.get('/minha-conta')
def render_minha_conta():
	return render_template('minha_conta.html')

