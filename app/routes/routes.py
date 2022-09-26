from app import app

@app.route('/home', methods=['GET'])
def home_route():
	return '<h1>Home</h1>'