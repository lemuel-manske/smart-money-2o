from flask import jsonify, Blueprint

from app.utils.choices import Moedas, Instituicoes, TipoTransacao


home_routes = Blueprint('home_routes', __name__)

@home_routes.route('/', methods=['GET'])
def home_route():
	'''
	Rota home/padrão.

	'''
	return '<a href="https://github.com/lemuel-manske/smart-money-2o">docs</a>'


@home_routes.route('/enum', methods=['GET'])
def rota_informacoes_enum():
	'''
	Retorna classes enumeradores existentes.
	'''
	enums = [Moedas, Instituicoes, TipoTransacao]

	res = [enum.repr() for enum in enums]

	return jsonify(res)