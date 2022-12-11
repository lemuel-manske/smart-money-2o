from flask import jsonify, Blueprint, render_template

from app.utils.choices import Moedas, Instituicoes, TipoTransacao
from app.utils import response


home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def home_route():
	return render_template('home.html', title='Home')


@home.route('/enum/<string:classe>', methods=['GET'])
def rota_informacoes_enum(classe: str):
	'''
	Retorna classes enumeradores existentes.
	'''
	
	resultado = None

	if classe == 'moedas':
		resultado = Moedas.to_json()
	elif classe == 'tipo-transacao':
		resultado = TipoTransacao.to_json()
	elif classe == 'instituicao-bancaria':
		resultado = Instituicoes.to_json()
	else:	
		return response(404, 'Nenhuma classe encontrada com o nome informado.')

	return jsonify(resultado)
