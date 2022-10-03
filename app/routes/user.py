from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app import app
from app.models import Usuario

@app.route('/login', methods=['POST'])
def login_route():
	auth_data = request.get_json()
	email = auth_data['email']

	return email
