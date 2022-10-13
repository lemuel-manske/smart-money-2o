from app import app

@app.route('/home', methods=['GET'])
def home_route():
	'''
	Rota home/padrão.
	'''
	return '<h1>Home</h1>'

# TODO: criacao de conta bancaria