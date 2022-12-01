const fields = {
	login: {
		email: '#email-login',
		senha: '#senha-login'
	},
	cadastro: {
		email: '#email-cadastro',
		nome: '#nome-cadastro',
		senha: '#senha-cadastro'
	}
}

jQuery(function($) {

	cleanErrors();

	$('#login-submit').on('click', function() {
		login_fields = fields.login;

		let [ email, senha ] = get_fields_values(login_fields.email, login_fields.senha)

		is_error = !completed_fieds(
			login_fields.email,
			login_fields.senha)
		
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

				success: () => {
					location.pathname = '/';
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					showError(login_fields[response.target], response.msg);
				}
			})
		}
	})

	$('#cadastro-submit').on('click', function () {
		cadastro_fields = fields.cadastro;

		let [ email, nome, senha ] = get_fields_values(cadastro_fields.email, cadastro_fields.nome, cadastro_fields.senha)

		let is_error = !completed_fieds(
			cadastro_fields.email,
			cadastro_fields.nome,
			cadastro_fields.senha
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

				success: () => {
					location.pathname = '/'
				},
				
				error: (xhr) => {
					response = xhr.responseJSON;
					showError(cadastro_fields[response.target], response.msg);
				}
			})
		}
	})
})