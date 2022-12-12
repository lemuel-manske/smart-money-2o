const LOGIN_FIELDS = {
	email: '#email-login',
	senha: '#senha-login'
}

const CADASTRO_FIELDS = {
	email: '#email-cadastro',
	nome: '#nome-cadastro',
	senha: '#senha-cadastro'
}

jQuery(function($) {

	removeErrors();

	$('#login-submit').on('click', function() {
		let [ email, senha ] = getFieldsValues(LOGIN_FIELDS.email, LOGIN_FIELDS.senha)

		is_error = !completedFields(
			LOGIN_FIELDS.email,
			LOGIN_FIELDS.senha)
		
		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/auth/login',
				method: 'POST',
				
				contentType: 'application/json',
				dataType: 'json',
				data: JSON.stringify({
					email: email,
					senha: senha
				}),
				
				success: (res) => {
					setMoeda()

					location.pathname = '/app/';
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					showError(LOGIN_FIELDS[response.target], response.msg);
				}
			})
		}
	})

	$('#cadastro-submit').on('click', function () {
		let [ email, nome, senha ] = getFieldsValues(CADASTRO_FIELDS.email, CADASTRO_FIELDS.nome, CADASTRO_FIELDS.senha)

		let is_error = !completedFields(
			CADASTRO_FIELDS.email,
			CADASTRO_FIELDS.nome,
			CADASTRO_FIELDS.senha
		)

		if (!is_error) {
			$.ajax({
				url: 'http://localhost:5000/api/auth/cadastro',
				method: 'POST',
				
				contentType: 'application/JSON',
				dataType: 'json',
				data: JSON.stringify({
					email: email,
					nome: nome,
					senha: senha
				}),

				success: (res) => {
					setMoeda()

					location.pathname = '/app/';
				},
				
				error: (xhr) => {
					response = xhr.responseJSON;
					showError(CADASTRO_FIELDS[response.target], response.msg);
				}
			})
		}
	})
})