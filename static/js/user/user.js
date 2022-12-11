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

	remover_erros();

	$('#login-submit').on('click', function() {
		let [ email, senha ] = get_fields_values(LOGIN_FIELDS.email, LOGIN_FIELDS.senha)

		is_error = !completed_fieds(
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
					set_user_moeda()

					location.pathname = '/app/';
				},

				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(LOGIN_FIELDS[response.target], response.msg);
				}
			})
		}
	})

	$('#cadastro-submit').on('click', function () {
		let [ email, nome, senha ] = get_fields_values(CADASTRO_FIELDS.email, CADASTRO_FIELDS.nome, CADASTRO_FIELDS.senha)

		let is_error = !completed_fieds(
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
					set_user_moeda()

					location.pathname = '/app/';
				},
				
				error: (xhr) => {
					response = xhr.responseJSON;
					show_error(CADASTRO_FIELDS[response.target], response.msg);
				}
			})
		}
	})
})