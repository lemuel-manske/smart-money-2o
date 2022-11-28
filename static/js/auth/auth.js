const fields = {
	login: {
		email: '#email-login',
		senha: '#senha-login'
	},
	cadastro: {
		nome: '#nome-cadastro',
		nome: '#email-cadastro',
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
})