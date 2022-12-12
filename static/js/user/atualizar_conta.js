const ATUALIZAR_CONTA_FIELDS = {
	email: '#email-atualizar',
	nome: '#nome-atualizar',
	senha: '#senha-atual-atualizar',
	senha_nova: '#senha-nova-atualizar',
	moedas_select: "#moedas-atualizar"
}

jQuery(function($) {

	removeErrors();

	$.ajax({
		url: 'http://localhost:5000/enum/moedas',
		method: 'GET',
		
		success: (res) => {
			let dados = (JSON.parse(JSON.stringify(res)));

			let moedas = dados.msg.Moedas;

			$.each(moedas, function (i, moeda) {
				$(ATUALIZAR_CONTA_FIELDS.moedas_select).append(
					$('<option>', {
						value: i,
						text: moeda,
					})
				)
			})	
		}
	})

	$.ajax({
		url: 'http://localhost:5000/api/user/minha-conta',
		method: 'GET',
		
		success: (res) => {
			let dados = (JSON.parse(JSON.stringify(res)));

			$(ATUALIZAR_CONTA_FIELDS.email).append(dados.msg.email);
			$(ATUALIZAR_CONTA_FIELDS.nome).val(dados.msg.nome);
		}
	})

	$('#atualizar-submit').on('click', function () {
		atualizar_fields = ATUALIZAR_CONTA_FIELDS;
		
		let [ nome, senha, senha_nova ] = getFieldsValues(atualizar_fields.nome, atualizar_fields.senha,
				atualizar_fields.senha_nova)
		let [ moeda ] = getSelectFieldsValues(atualizar_fields.moedas_select)
		
		let is_error = !completedFields(
			atualizar_fields.nome,
			atualizar_fields.senha,
			atualizar_fields.senha_nova
			)
			
		if (!is_error) {
			console.log('1')
			$.ajax({
				url: 'http://localhost:5000/api/user/atualizar-conta',
				method: 'POST',
				xhrFields: {
					withCredentials: true
				},
				headers: {
					'X-CSRF-TOKEN':getCookie('csrf_access_token')
				},
				
				contentType: 'application/JSON',
				dataType: 'json',
				data: JSON.stringify({
					nome: nome,
					senha: senha,
					nova_senha: senha_nova,
					moeda: moeda
				}),

				success: (res) => {
					localStorage.setItem('moeda', res.msg.moeda);
					location.reload();
				},
				
				error: (xhr) => {
					response = xhr.responseJSON;
					showError(atualizar_fields[response.target], response.msg);
				}
			})
		}
	})
})