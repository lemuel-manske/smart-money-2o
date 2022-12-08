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

	clean_errors();

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
				
				success: (res) => {
					token = res.msg;
					localStorage.setItem('x-sm-update-bearer-token', token);
				
					location.pathname = '/app/';
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(login_fields[response.target], response.msg);
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

				success: (res) => {
					token = res.msg;
					sessionStorage.setItem('x-sm-update-bearer-token', accessToken);
					location.pathname = '/app/';
				},
				
				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(cadastro_fields[response.target], response.msg);
				}
			})
		}
	})
})