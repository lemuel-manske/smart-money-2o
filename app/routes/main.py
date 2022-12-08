from flask import Blueprint, render_template

main = Blueprint('main', __name__, url_prefix='/app')

@main.get('/')
def render_dashboard():
	return render_template('dashboard.html', title='Dashboard', currency_symbol='R$')

@main.get('/t')
def render_teste():
	return render_template('teste.html', title='Teste')