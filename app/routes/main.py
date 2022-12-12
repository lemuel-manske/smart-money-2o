from flask import Blueprint, render_template

from app.decorators import check_for_jwt


main_render = Blueprint('main_render', __name__, url_prefix='/app')

@main_render.get('/')
@check_for_jwt
def render_dashboard():
	'''
	Rota dashboard (painel de controle).

	É a página principal da aplicação, o "rosto" do aplicativo.
	'''
	return render_template('dashboard.html', title='Dashboard')

@main_render.get('/historico')
@check_for_jwt
def render_historico():
	'''
	Rota histórico.

	Reúne uma listagem dos dados do usuário, como 
	contas bancárias, transações e transferências bancárias
	em tabelas.
	'''
	return render_template('historico.html', title='Histórico')