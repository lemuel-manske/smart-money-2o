from flask import Blueprint, render_template

from app.decorators import check_for_jwt

main = Blueprint('main', __name__, url_prefix='/app')

@main.get('/')
@check_for_jwt
def render_dashboard():
	return render_template('dashboard.html', title='Dashboard')

@main.get('/historico')
@check_for_jwt
def render_historico():
	return render_template('historico.html', title='Histórico')