from flask import Blueprint, render_template

from app.utils import response
from app.utils.enums import Moedas, Instituicoes, TipoTransacao


home_render = Blueprint('home_render', __name__)

@home_render.get('/')
def home_route():
	'''
	Rota padrão (home) da aplicação.
	'''
	return render_template('home.html', title='Home')


@home_render.get('/enum/<string:classe>')
def rota_informacoes_enum(classe: str):
	'''
	Retorna classes enumeradores existentes.

	Args:
		classe: str - classe `Enum` a ser exibida.
	
	Returns:
		CÓD. 404 (NOT_FOUND): Classe não encontrada;
		CÓD. 200 (OK): Sucesso - retorna a classe em formato json.
	'''
	enums = {
		'moedas': Moedas.to_json(),
		'tipo-transacao': TipoTransacao.to_json(),
		'instituicao-bancaria': Instituicoes.to_json(),
	}

	if classe in enums.keys():
		return response(200, enums[classe])

	return response(404, 'Nenhuma classe encontrada com o nome informado.')
