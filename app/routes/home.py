from flask import jsonify, Blueprint, render_template

from app.utils.choices import Moedas, Instituicoes, TipoTransacao


home = Blueprint('home_routes', __name__)

@home.route('/', methods=['GET'])
def home_route():
	return render_template('home.html', title='Home')


@home.route('/enum', methods=['GET'])
def rota_informacoes_enum():
	'''
	Retorna classes enumeradores existentes.
	'''
	enums = [Moedas, Instituicoes, TipoTransacao]

	res = [enum.repr() for enum in enums]

	return jsonify(res)