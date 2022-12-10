from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

from app.decorators import requer_login

main = Blueprint('main', __name__, url_prefix='/app')

@main.get('/')
@requer_login
def render_dashboard():
	return render_template('dashboard.html', title='Dashboard', currency_symbol='R$')

@main.get('/t')
def render_teste():
	return render_template('teste.html', title='Teste')